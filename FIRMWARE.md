# Galaxy 100 firmware: bootloader, flashing, and recovery

## Hardware

- **MCU:** Westberry WB32FQ95 (ARM-based, but a proprietary Chinese chip — not STM32, not Atmel)
- **Bootloader:** `wb32-dfu` (Westberry-specific DFU). **Standard `dfu-util` will not flash this board.**
- **Flash tool needed locally:** `wb32-dfu-updater_cli` (from [WestberryTech/wb32-dfu-updater](https://github.com/WestberryTech/wb32-dfu-updater))
- **LEDs:** 100 (99 keys + 1 battery indicator), WS2812-compatible, SPI-driven on pin B15
- **VID:PID:** `0x36B0:0x30D4` (factory shipped — overridden in our `keyboard.json` to keep this stable so the [keeb CLI](https://github.com/ibeandrew/keeb) keeps working). The upstream Epomaker GitHub repo declares `0x342D:0xE489`, which we explicitly do **not** want to change to.

## Bootloader entry (DFU mode)

Three independent ways. Use whichever is easiest given the board's current state:

1. **PCB reset button** (most reliable): unplug, then **hold the reset switch on the bottom of the PCB** while plugging USB-C back in. Works even if firmware is bricked.
2. **Hold Escape on plug-in**: unplug, then plug in while holding `Escape`. **Note: this also wipes EEPROM** (keymap, macros, RGB recordings, etc.). Use the keeb backup snapshot if you want to restore.
3. **Fn + R_Shift + Esc** keychord: only works if the currently-flashed firmware honors it (default QMK does). If you flash a broken firmware, fall back to method 1.

While in DFU mode the keyboard appears as a different USB device — typically `WB32 DFU` or similar. Check with PowerShell:

```powershell
Get-PnpDevice -PresentOnly | Where-Object { $_.FriendlyName -match 'wb32|dfu' } | Format-List FriendlyName,InstanceId
```

## Flashing

```powershell
# After downloading the build artifact and putting board into DFU mode:
wb32-dfu-updater_cli -D galaxy100_default.bin
```

`wb32-dfu-updater_cli` is bundled with QMK MSYS, but you can also grab it standalone (user-scope, no admin) from [WestberryTech releases](https://github.com/WestberryTech/wb32-dfu-updater/releases) and drop it on PATH (e.g. `~/.local/bin`).

## Recovery (if a flash bricks the board)

The Westberry bootloader is **separate from** the application firmware — it lives in a protected flash region and can't be overwritten by `wb32-dfu-updater_cli`. As long as you can trigger DFU mode (method 1 above is hardware-level and always works), you can re-flash any working firmware. There is no "permanently bricked" state we can reach through normal flashing operations.

If method 1 stops working, the bootloader itself is corrupted, which would require Westberry-specific recovery hardware. Don't expect to encounter this through normal use.

## Pre-flash checklist

Before every flash, run [scripts/backup.py in the keeb repo](https://github.com/ibeandrew/keeb/blob/main/scripts/backup.py) to dump the current keymap, macros, and RGB state to JSON. This is your snapshot for restoring user-facing state after a flash.

```powershell
cd C:\Users\amoore1\keeb
uv run python scripts/backup.py "backups/pre-flash-$(Get-Date -Format 'yyyyMMdd-HHmmss').json"
```
