/*
 * Custom linker script for Galaxy 100 with RDMCTMZT bootloader.
 *
 * CRITICAL: Epomaker's factory firmware is linked at flash base 0x00000000,
 * NOT the STM32-standard 0x08000000 that upstream chibios-contrib defaults to.
 * Confirmed by analyzing the factory .bin Epomaker support sent: vector table
 * has reset handler = 0x00000191, NMI = 0x0000d49d, all handlers in 0x000000xx
 * range. The WB32FQ95 in this OEM's boot configuration maps flash at 0x00000000.
 *
 * Total flash on WB32FQ95xB: 128KB. Factory firmware is ~71KB, leaving ~57KB
 * for the bootloader at the high end of flash (0x00012000 - 0x00020000).
 */

MEMORY
{
    flash0 (rx) : org = 0x00000000, len = 72k
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
