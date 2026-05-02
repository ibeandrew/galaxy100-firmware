RGB_MATRIX_CUSTOM_USER = yes
include keyboards/epomaker/galaxy100/rgb_record/rgb_record.mk

# Use our custom linker script with app at 0x08008000 (skipping RDMCTMZT bootloader region)
MCU_LDSCRIPT = WB32FQ95-app

