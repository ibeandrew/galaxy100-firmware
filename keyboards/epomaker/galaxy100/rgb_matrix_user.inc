// Copyright 2024 Epomaker (@Epomaker)
// SPDX-License-Identifier: GPL-2.0-or-later

#ifdef ENABLE_RGB_MATRIX_RGBR_PLAY
RGB_MATRIX_EFFECT(RGBR_PLAY)
#    ifdef RGB_MATRIX_CUSTOM_EFFECT_IMPLS

bool RGBR_PLAY(effect_params_t *params) {
    RGB_MATRIX_USE_LIMITS(led_min, led_max);

    extern void rgbrec_play(uint8_t led_min, uint8_t led_max);
    rgbrec_play(led_min, led_max);

    return rgb_matrix_check_finished_leds(led_max);
}

#    endif // RGB_MATRIX_CUSTOM_EFFECT_IMPLS
#endif

/* Phase 1 smoke test: static checkerboard of red and blue, no animation.
   Pure pipeline validator - if you can see this on the board, the whole
   fork -> CI build -> flash chain is working end-to-end. */
#ifdef ENABLE_RGB_MATRIX_KEEB_TEST_CHECKERBOARD
RGB_MATRIX_EFFECT(KEEB_TEST_CHECKERBOARD)
#    ifdef RGB_MATRIX_CUSTOM_EFFECT_IMPLS

bool KEEB_TEST_CHECKERBOARD(effect_params_t *params) {
    RGB_MATRIX_USE_LIMITS(led_min, led_max);

    for (uint8_t i = led_min; i < led_max; i++) {
        uint8_t cell_x = g_led_config.point[i].x / 32;
        uint8_t cell_y = g_led_config.point[i].y / 32;
        if ((cell_x + cell_y) & 1) {
            rgb_matrix_set_color(i, 255, 0, 0);
        } else {
            rgb_matrix_set_color(i, 0, 0, 255);
        }
    }

    return rgb_matrix_check_finished_leds(led_max);
}

#    endif // RGB_MATRIX_CUSTOM_EFFECT_IMPLS
#endif
