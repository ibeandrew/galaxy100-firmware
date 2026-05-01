# galaxy100-firmware

Custom QMK firmware for the **Epomaker Galaxy 100 (QMK/VIA edition)**, with extra RGB matrix effects that aren't possible through VIA's host-side protocol.

## Why this exists

VIA only exposes one HSV color globally — there's no way to drive per-key colors from the host PC. Effects that need per-key color (animated fills, multi-color palettes, etc.) have to live in the firmware itself.

## How it works

This repo contains only the modified Galaxy 100 keyboard files. CI assembles the full firmware in GitHub Actions:

1. Clone upstream `qmk/qmk_firmware` (has WB32FQ95 MCU support)
2. Overlay our `keyboards/epomaker/galaxy100/` directory
3. `qmk compile -kb epomaker/galaxy100 -km default`
4. Upload the resulting `.bin` as a build artifact

You download the artifact, flash it to your keyboard with `wb32-dfu-updater_cli`, done.

## Adding a new RGB effect

Add the effect to [`keyboards/epomaker/galaxy100/rgb_matrix_user.inc`](keyboards/epomaker/galaxy100/rgb_matrix_user.inc) following the existing `RGBR_PLAY` pattern. Then enable it via `#define ENABLE_RGB_MATRIX_<YOUR_EFFECT_NAME>` in [`config.h`](keyboards/epomaker/galaxy100/config.h).

## Flashing

See [FIRMWARE.md](FIRMWARE.md) for the full bootloader / recovery procedure.
