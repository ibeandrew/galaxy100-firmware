"""Probe the RDMCTMZT DFU HID-vendor endpoint for any documented protocol response.

The DFU device exposes both Mass Storage AND a HID-vendor-defined endpoint at
VID 0x03EB PID 0x2045 interface 1, usage_page 0xFF00. We've ruled out the MSC
side as the source of our flash-and-not-boot failures. Maybe the HID side
speaks a documented protocol (LUFA HID Bootloader has a standard one).

This script probes by sending various OUT/feature reports and reading any
INPUT/feature response. If we get any meaningful echo it tells us:
  - whether the protocol is LUFA HID Bootloader compatible
  - or some custom RDMCTMZT thing we'd have to reverse engineer
"""
from __future__ import annotations

import time
import hid

VID = 0x03EB
PID = 0x2045


def find_iface() -> bytes | None:
    for d in hid.enumerate(VID, PID):
        if d.get("usage_page") == 0xFF00:
            print(f"found vendor HID iface: {d['path']!r}")
            print(f"  product={d.get('product_string')!r}  mfr={d.get('manufacturer_string')!r}")
            print(f"  iface={d.get('interface_number')}  usage_page=0x{d.get('usage_page',0):04X}  usage=0x{d.get('usage',0):04X}")
            return d["path"]
    return None


def hexdump(b: bytes, prefix: str = "  ") -> str:
    if not b:
        return f"{prefix}<empty>"
    out = []
    for i in range(0, len(b), 16):
        chunk = b[i:i+16]
        hexs = " ".join(f"{x:02x}" for x in chunk)
        ascii_ = "".join(chr(x) if 32 <= x < 127 else "." for x in chunk)
        out.append(f"{prefix}{i:04x}  {hexs:<48}  {ascii_}")
    return "\n".join(out)


def try_feature_read(path: bytes) -> None:
    print("\n=== feature reports ===")
    h = hid.device()
    h.open_path(path)
    for rid in range(0, 8):
        try:
            r = h.get_feature_report(rid, 64)
            if r and any(r):
                print(f"feature {rid}: ({len(r)} bytes)")
                print(hexdump(bytes(r)))
            else:
                print(f"feature {rid}: empty/zero")
        except Exception as e:
            print(f"feature {rid}: {e}")
    h.close()


def try_lufa_hid_bootloader_query(path: bytes) -> None:
    """LUFA HID Bootloader commands.
    Standard message format: 32-byte OUT report.
    Address word + data, last byte 0xFF means 'flash write done' (jump to app).
    Try to read flash by querying various known endpoints.
    """
    print("\n=== LUFA HID Bootloader-style probes ===")
    h = hid.device()
    h.open_path(path)
    h.set_nonblocking(False)

    # try empty/zero output report
    try:
        report = bytes([0x00] * 33)  # report ID 0x00 + 32 data bytes
        n = h.write(report)
        print(f"write zero report -> n={n}")
        time.sleep(0.05)
        r = h.read(64, timeout_ms=200)
        print(f"read after zero: {hexdump(bytes(r)) if r else '<no reply>'}")
    except Exception as e:
        print(f"zero probe: {e}")

    # try a "version query" or similar - commonly 0x01 0x00 ...
    for query in [
        bytes([0x00, 0x01]),  # version-like
        bytes([0x00, 0x10]),  # info
        bytes([0x00, 0x20]),  # status
        bytes([0x00, 0xFE]),  # boot-magic-ish
        bytes([0x00, 0xFF]),  # exit-bootloader-ish
        b"\x00" + b"info" + b"\x00" * 27,  # ASCII probe
        b"\x00" + b"DFU?" + b"\x00" * 27,
    ]:
        try:
            payload = (query + b"\x00" * 33)[:33]
            n = h.write(payload)
            time.sleep(0.05)
            r = h.read(64, timeout_ms=200)
            label = " ".join(f"{x:02x}" for x in query[:8])
            print(f"send [{label}...] -> n={n}, reply={hexdump(bytes(r)) if r else '<no reply>'}")
        except Exception as e:
            print(f"probe {query[:4]!r}: {e}")

    h.close()


def main() -> None:
    path = find_iface()
    if not path:
        print("DFU HID interface not found - is keyboard in DFU mode?")
        return
    try_feature_read(path)
    try_lufa_hid_bootloader_query(path)


if __name__ == "__main__":
    main()
