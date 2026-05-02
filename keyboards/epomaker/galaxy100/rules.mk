# Force the app's .text/.startup section to start past the RDMCTMZT bootloader
# (assumed at 0x08000000 for 32KB). This overrides where the linker places
# our vector table without needing a full custom linker script (which breaks
# QMK's MCU detection logic).
EXTRALDFLAGS += -Wl,--section-start=.startup=0x08008000
