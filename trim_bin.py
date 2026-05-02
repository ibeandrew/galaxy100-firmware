"""Strip leading zero padding from a relocated firmware .bin.

The linker produces a flat .bin where address 0 -> highest section addr;
when we link at 0x08008000 (etc.) the leading bytes are zero filler.
This trims those off so the bootloader gets the actual code at offset 0.
"""
import struct
import sys


def main() -> None:
    raw_path, out_path, skip_str = sys.argv[1:4]
    skip = int(skip_str, 0)
    data = open(raw_path, "rb").read()
    trimmed = data[skip:]
    open(out_path, "wb").write(trimmed)
    sp, reset = struct.unpack("<II", trimmed[:8])
    print(f"  raw={len(data)} trimmed={len(trimmed)} SP=0x{sp:08X} reset=0x{reset:08X}")


if __name__ == "__main__":
    main()
