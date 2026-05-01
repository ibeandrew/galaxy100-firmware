/* Stub implementation of Epomaker's per-key RGB recording feature.
 *
 * Original rgb_record.c relies on EECONFIG_USER_DATABLOCK / EECONFIG_BASE_SIZE
 * macros that exist only in Epomaker's QMK fork. Since we're not using the
 * recording feature (it's a Fn-key triggered manual capture-and-replay flow),
 * we replace the bodies with no-ops to break the dependency on the fork.
 *
 * galaxy100.c calls these functions for indicator/input handling and assumes
 * sane defaults when "no recording is active", which is what the stubs return.
 */

#include "rgb_record.h"

void rgbrec_init(uint8_t channel) {
    (void)channel;
}

bool rgbrec_is_started(void) {
    return false;
}

bool rgbrec_register_record(uint16_t keycode, keyrecord_t *record) {
    (void)keycode;
    (void)record;
    return false;
}

void rgbrec_read_current_channel(uint8_t channel) {
    (void)channel;
}

bool rgbrec_end(uint8_t channel) {
    (void)channel;
    return false;
}

bool rgbrec_show(uint8_t channel) {
    (void)channel;
    return false;
}

bool rgbrec_start(uint8_t channel) {
    (void)channel;
    return false;
}

void rgbrec_set_close_all(uint8_t h, uint8_t s, uint8_t v) {
    (void)h;
    (void)s;
    (void)v;
}

void rgbrec_play(uint8_t led_min, uint8_t led_max) {
    (void)led_min;
    (void)led_max;
}

void eeconfig_init_user_datablock(void) {
}

void record_rgbmatrix_increase(uint8_t *last_mode) {
    (void)last_mode;
}

void record_color_hsv(bool status) {
    (void)status;
}

void query(void) {
}
