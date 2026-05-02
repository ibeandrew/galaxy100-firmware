"""Post-build vector table relocator.

Reads a raw ARM Cortex-M firmware .bin (linked at 0x08000000) and adjusts
absolute pointers in the vector table so the firmware can be loaded at a
different flash offset without re-linking. Specifically: every 32-bit word
in the vector table that looks like a code address gets shifted by `--shift`.

This is a hack. Internal code uses PC-relative branches so it works fine
when loaded at the new offset, but absolute pointers in .data/.rodata
(function pointer arrays, init lists, etc.) are NOT touched. For simple
firmware (RGB effect tests) this is usually enough to boot.
"""
from __future__ import annotations

import argparse
import struct
from pathlib import Path


def patch(in_path: Path, out_path: Path, shift: int, vt_words: int = 64) -> None:
    data = bytearray(in_path.read_bytes())
    if len(data) < vt_words * 4:
        raise SystemExit(f"binary too small ({len(data)} bytes)")

    # ARM Cortex-M flash is at 0x08000000 (typical). Patch any word in the
    # vector table that points into [0x08000000, 0x08000000 + 0x40000).
    flash_lo = 0x08000000
    flash_hi = 0x08000000 + 0x40000  # 256KB max we care about

    print(f"shift = 0x{shift:X}")
    print(f"first {vt_words} vector table words:")
    patched = 0
    for i in range(vt_words):
        off = i * 4
        v = struct.unpack_from("<I", data, off)[0]
        # vector[0] is initial SP (RAM) — never a code address, skip.
        if i == 0:
            print(f"  [{i:2d}] 0x{v:08X} (SP, unchanged)")
            continue
        if flash_lo <= v < flash_hi:
            new = v + shift
            struct.pack_into("<I", data, off, new)
            print(f"  [{i:2d}] 0x{v:08X} -> 0x{new:08X}")
            patched += 1
        elif v != 0:
            print(f"  [{i:2d}] 0x{v:08X} (not in flash range, unchanged)")

    print(f"\npatched {patched} vector entries")
    out_path.write_bytes(data)
    print(f"wrote: {out_path}  ({len(data)} bytes)")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("input", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--shift", type=lambda s: int(s, 0), default=0x8000,
                   help="amount to add to flash addresses (default 0x8000)")
    p.add_argument("--vt-words", type=int, default=64,
                   help="how many words of vector table to scan (default 64)")
    args = p.parse_args()
    patch(args.input, args.output, args.shift, args.vt_words)


if __name__ == "__main__":
    main()
