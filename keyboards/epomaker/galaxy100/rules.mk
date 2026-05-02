# Galaxy 100: custom linker script at ./ld/WB32FQ95xB.ld with app at 0x08008000
# (skipping the OEM RDMCTMZT bootloader region).
#
# When we provide our own LDSCRIPT, QMK's platform.mk skips the
# chibios-contrib fallback branch that normally sets USE_CHIBIOS_CONTRIB=yes
# as a side effect. Without that flag, the WB32 chip support headers
# (hal_lld.h etc.) don't get added to include paths and the build fails.
# Explicitly set it here to keep includes working.
USE_CHIBIOS_CONTRIB = yes
