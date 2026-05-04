"""HID probe v2: broader report IDs and direct read() instead of feature reports."""
from __future__ import annotations

import struct
import time

import hid


VID = 0x03EB
PID = 0x2045


def hexdump(b: bytes, prefix: str = "  ") -> str:
    if not b:
        return f"{prefix}<empty>"
    out = []
    for i in range(0, min(len(b), 64), 16):
        chunk = b[i:i + 16]
        hexs = " ".join(f"{x:02x}" for x in chunk)
        ascii_ = "".join(chr(x) if 32 <= x < 127 else "." for x in chunk)
        out.append(f"{prefix}{i:04x}  {hexs:<48}  {ascii_}")
    return "\n".join(out)


def main() -> None:
    path = None
    for d in hid.enumerate(VID, PID):
        if d.get("usage_page") == 0xFF00:
            path = d["path"]
            break
    if not path:
        print("DFU HID interface not found")
        return

    print(f"opening {path!r}")
    h = hid.device()
    h.open_path(path)
    h.set_nonblocking(True)

    # Try direct READ (in case the device is sending something unsolicited)
    print("\n=== unsolicited reads (300ms total) ===")
    end = time.time() + 0.3
    while time.time() < end:
        r = h.read(64, timeout_ms=50)
        if r:
            print(f"  got {len(r)} bytes: {hexdump(bytes(r))}")
    print("  (silent)")

    # Try writing single-byte test reports across all report IDs
    print("\n=== single-byte writes across report IDs 0-255 ===")
    successful_writes = []
    for rid in range(256):
        try:
            payload = bytes([rid]) + b"\x00" * 32  # 33-byte report (1 ID + 32 data)
            n = h.write(payload)
            if n > 0:
                successful_writes.append(rid)
                # Try reading immediately after a successful write
                time.sleep(0.01)
                r = h.read(64, timeout_ms=50)
                if r:
                    print(f"  rid 0x{rid:02x}: WROTE {n} bytes, got reply: {hexdump(bytes(r))}")
        except Exception:
            pass

    print(f"\nsuccessful writes on {len(successful_writes)} report IDs")
    if successful_writes:
        print(f"first 20: {successful_writes[:20]}")

    # Try feature reports for IDs 0-255
    print("\n=== feature reads across report IDs 0-255 ===")
    successful_reads = []
    for rid in range(256):
        try:
            r = h.get_feature_report(rid, 64)
            if r and any(r):
                successful_reads.append((rid, bytes(r)))
        except Exception:
            pass
    print(f"successful feature reads on {len(successful_reads)} report IDs")
    for rid, data in successful_reads[:8]:
        print(f"  rid 0x{rid:02x}: {hexdump(data)}")

    h.close()


if __name__ == "__main__":
    main()
