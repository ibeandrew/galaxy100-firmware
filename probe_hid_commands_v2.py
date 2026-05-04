"""Deeper probe of RDMCTMZT bootloader HID protocol on report 0x3F.

Findings so far:
- Baseline (all-zero payload): `3f aa c0 00 80 01 00 01 40 00 ...`
- cmd byte 0xAA in payload: `3f aa c0 00 80 01 00 04 45 00 ...` (bytes 7-8 changed)

Strategy:
1. Try 2-byte command pairs at payload[0:2]
2. Try common bootloader magic numbers
3. Try LUFA HID Bootloader format ([addr_lo, addr_hi, data...])
4. Try address-style payloads to provoke read-flash responses
"""
from __future__ import annotations

import time

import hid

VID = 0x03EB
PID = 0x2045


def open_iface():
    for d in hid.enumerate(VID, PID):
        if d.get("usage_page") == 0xFF00:
            h = hid.device()
            h.open_path(d["path"])
            h.set_nonblocking(False)
            return h
    raise SystemExit("DFU HID interface not found")


def hexdump(b, prefix=""):
    if not b:
        return f"{prefix}<empty>"
    out = []
    for i in range(0, min(len(b), 64), 16):
        chunk = b[i:i + 16]
        hexs = " ".join(f"{x:02x}" for x in chunk)
        ascii_ = "".join(chr(x) if 32 <= x < 127 else "." for x in chunk)
        out.append(f"{prefix}{i:04x}  {hexs:<48}  {ascii_}")
    return "\n".join(out)


def send(h, payload, timeout_ms=200):
    report = bytes([0x3F]) + payload + b"\x00" * (64 - len(payload))
    h.write(report[:65])
    time.sleep(0.005)
    r = h.read(64, timeout_ms=timeout_ms)
    return bytes(r) if r else b""


def main():
    h = open_iface()

    base = send(h, b"")
    print("=== baseline ===")
    print(hexdump(base))

    # Common bootloader magic byte patterns
    magic_patterns = [
        ("0x55 0xAA", b"\x55\xaa"),
        ("0xAA 0x55", b"\xaa\x55"),
        ("0xDE 0xAD", b"\xde\xad"),
        ("0xCA 0xFE", b"\xca\xfe"),
        ("0xFF 0xFF", b"\xff\xff"),
        ("0x00 0xAA", b"\x00\xaa"),
        ("0x10 0x00", b"\x10\x00"),
        ("0xAA 0x01", b"\xaa\x01"),
        ("0xAA 0x02", b"\xaa\x02"),
        ("0xAA 0x10", b"\xaa\x10"),
        ("0xAA 0x55", b"\xaa\x55"),
        ("0xAA 0xAA", b"\xaa\xaa"),
        ("0xAA 0xC0", b"\xaa\xc0"),
        ("0xAA 0xFF", b"\xaa\xff"),
        ("ascii 'INFO'", b"INFO"),
        ("ascii 'QUERY'", b"QUERY"),
        ("ascii 'GET'", b"GET"),
        ("ascii 'BOOT'", b"BOOT"),
        ("ascii 'PING'", b"PING"),
        ("ascii 'READ'", b"READ"),
        # LUFA HID Bootloader format: addr_le, then data
        ("addr 0x00000000", b"\x00\x00\x00\x00"),
        ("addr 0x08000000", b"\x00\x00\x00\x08"),
        ("addr 0x0801A000", b"\x00\xa0\x01\x08"),
        # Single-byte responses
        ("byte 0x10", b"\x10"),
        ("byte 0x20", b"\x20"),
        ("byte 0x30", b"\x30"),
        ("byte 0x40", b"\x40"),
        ("byte 0x50", b"\x50"),
        ("byte 0x60", b"\x60"),
        ("byte 0x70", b"\x70"),
        ("byte 0x80", b"\x80"),
        ("byte 0x90", b"\x90"),
        ("byte 0xC0", b"\xc0"),
        ("byte 0xE0", b"\xe0"),
        # 0xAA followed by various
        ("0xAA + zeros (cmd ack?)", b"\xaa" + b"\x00" * 4),
    ]

    print("\n=== probing magic patterns ===")
    distinct = {}
    for label, payload in magic_patterns:
        r = send(h, payload)
        sig = r[:16] if r else b""
        if sig != base[:16]:
            distinct.setdefault(sig, []).append(label)

    if distinct:
        print(f"\n{len(distinct)} distinct response signatures:")
        for sig, labels in distinct.items():
            print(f"\nsignature: {sig.hex(' ')}")
            for lbl in labels:
                print(f"  triggered by: {lbl}")
    else:
        print("(no payload deviated from baseline)")

    # Look at the 0xAA response again, then try varying the SECOND byte after it
    print("\n=== fixing first byte = 0xAA, varying second byte 0-255 ===")
    aa_distinct = {}
    for b1 in range(256):
        r = send(h, bytes([0xaa, b1]))
        sig = r[:16] if r else b""
        aa_distinct.setdefault(sig, []).append(b1)
    print(f"distinct responses when [0]=0xAA, [1]=varies: {len(aa_distinct)}")
    for sig, b1_list in list(aa_distinct.items())[:6]:
        print(f"\n  sig: {sig.hex(' ')}")
        if len(b1_list) <= 5:
            print(f"    [1] values: {[hex(b) for b in b1_list]}")
        else:
            print(f"    [1] values: {len(b1_list)} variants ({hex(b1_list[0])}..{hex(b1_list[-1])})")

    h.close()


if __name__ == "__main__":
    main()
