# Use our custom linker script (in ./ld/) with app at 0x08008000 to skip
# the RDMCTMZT bootloader region. Filename matches the standard chip variant
# so QMK's MCU detection (hal_lld.h, etc.) keeps working.
MCU_LDSCRIPT = WB32FQ95xC
