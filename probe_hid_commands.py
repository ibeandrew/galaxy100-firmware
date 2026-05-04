"""Map the RDMCTMZT bootloader's HID command space.

We confirmed report ID 0x3F is responsive. Each report is 64 bytes (1 ID + 63 data).
Probe by varying the first DATA byte (likely a command byte) and looking at
how the response changes.
"""
from __future__ import annotations

import time

import hid

VID = 0x03EB
PID = 0x2045


def open_iface() -> hid.device:
    for d in hid.enumerate(VID, PID):
        if d.get("usage_page") == 0xFF00:
            h = hid.device()
            h.open_path(d["path"])
            h.set_nonblocking(False)
            return h
    raise SystemExit("DFU HID interface not found")


def hexdump(b: bytes, prefix: str = "") -> str:
    if not b:
        return f"{prefix}<empty>"
    out = []
    for i in range(0, len(b), 16):
        chunk = b[i:i + 16]
        hexs = " ".join(f"{x:02x}" for x in chunk)
        ascii_ = "".join(chr(x) if 32 <= x < 127 else "." for x in chunk)
        out.append(f"{prefix}{i:04x}  {hexs:<48}  {ascii_}")
    return "\n".join(out)


def send(h: hid.device, payload: bytes, read_size: int = 64, timeout_ms: int = 200) -> bytes:
    """Send a 64-byte data payload (report ID 0x3F prepended) and read response."""
    report = bytes([0x3F]) + payload + b"\x00" * (64 - len(payload))
    h.write(report[:65])  # report ID byte + 64 data bytes = 65 total
    time.sleep(0.01)
    r = h.read(read_size, timeout_ms=timeout_ms)
    return bytes(r) if r else b""


def main() -> None:
    h = open_iface()

    # Baseline: empty payload
    print("=== baseline (all-zero payload) ===")
    base = send(h, b"")
    print(hexdump(base, "  "))

    # Probe varying first data byte (likely command byte)
    print("\n=== command byte scan: payload=[CMD, 0x00*63] ===")
    print("(showing only responses that differ from baseline)")
    interesting = []
    for cmd in range(256):
        r = send(h, bytes([cmd]))
        if r != base:
            interesting.append((cmd, r))
            print(f"\ncmd 0x{cmd:02x}:")
            print(hexdump(r, "  "))
            if len(interesting) >= 20:
                print("\n(stopping after 20 distinct responses)")
                break

    if not interesting:
        print("(no command byte produced a response different from baseline)")

    # Try also varying second data byte while keeping first at 0
    print("\n=== second byte scan: payload=[0x00, CMD, 0x00*62] ===")
    interesting2 = []
    for cmd in range(0, 256, 1):
        r = send(h, bytes([0x00, cmd]))
        if r != base and (cmd, r) not in [(c, x) for c, x in interesting2]:
            interesting2.append((cmd, r))
            print(f"\nbyte[1] 0x{cmd:02x}:")
            print(hexdump(r, "  "))
            if len(interesting2) >= 10:
                print("\n(stopping after 10 distinct responses)")
                break
    if not interesting2:
        print("(byte[1] doesn't change response)")

    h.close()


if __name__ == "__main__":
    main()
