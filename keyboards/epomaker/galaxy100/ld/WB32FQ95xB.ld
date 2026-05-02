/*
 * Custom linker script for Galaxy 100 with RDMCTMZT bootloader.
 * Shifts app flash origin to 0x08008000 (32KB after start), reserving room
 * for the OEM bootloader. Total flash on WB32FQ95xB is 128KB.
 * Based on the ChibiOS-Contrib WB32FQ95xB.ld template.
 */

MEMORY
{
    flash0 (rx) : org = 0x08008000, len = 128k - 0x8000
    flash1 (rx) : org = 0x00000000, len = 0
    flash2 (rx) : org = 0x00000000, len = 0
    flash3 (rx) : org = 0x00000000, len = 0
    flash4 (rx) : org = 0x00000000, len = 0
    flash5 (rx) : org = 0x00000000, len = 0
    flash6 (rx) : org = 0x00000000, len = 0
    flash7 (rx) : org = 0x00000000, len = 0
    ram0 (wx)   : org = 0x20000000, len = 36k
    ram1 (wx)   : org = 0x00000000, len = 0
    ram2 (wx)   : org = 0x00000000, len = 0
    ram3 (wx)   : org = 0x00000000, len = 0
    ram4 (wx)   : org = 0x00000000, len = 0
    ram5 (wx)   : org = 0x00000000, len = 0
    ram6 (wx)   : org = 0x00000000, len = 0
    ram7 (wx)   : org = 0x00000000, len = 0
}

REGION_ALIAS("VECTORS_FLASH",     flash0);
REGION_ALIAS("VECTORS_FLASH_LMA", flash0);

REGION_ALIAS("XTORS_FLASH",     flash0);
REGION_ALIAS("XTORS_FLASH_LMA", flash0);

REGION_ALIAS("TEXT_FLASH",     flash0);
REGION_ALIAS("TEXT_FLASH_LMA", flash0);

REGION_ALIAS("RODATA_FLASH",     flash0);
REGION_ALIAS("RODATA_FLASH_LMA", flash0);

REGION_ALIAS("VARINIT_FLASH",     flash0);
REGION_ALIAS("VARINIT_FLASH_LMA", flash0);

REGION_ALIAS("MAIN_STACK_RAM",    ram0);
REGION_ALIAS("PROCESS_STACK_RAM", ram0);

REGION_ALIAS("DATA_RAM",     ram0);
REGION_ALIAS("DATA_RAM_LMA", flash0);

REGION_ALIAS("BSS_RAM",  ram0);
REGION_ALIAS("HEAP_RAM", ram0);

INCLUDE rules.ld
