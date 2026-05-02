# Galaxy 100: a custom linker script lives at ./ld/WB32FQ95xB.ld with
# app origin at 0x08008000 (skipping the RDMCTMZT bootloader region).
# QMK's MCU_LDSCRIPT default is WB32FQ95xB and the keyboard-local ld/
# directory takes precedence over chibios-contrib's, so just placing
# the file there is enough — no MCU_LDSCRIPT override needed here.
