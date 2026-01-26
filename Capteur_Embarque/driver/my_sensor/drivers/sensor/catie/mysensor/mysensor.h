/*
 * Copyright (c) 2025, CATIE
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef ZEPHYR_DRIVERS_SENSOR_MYSENSOR_MYSENSOR_H_
#define ZEPHYR_DRIVERS_SENSOR_MYSENSOR_MYSENSOR_H_

#include <zephyr/drivers/i2c.h>

#define MYSENSOR_START_UP_TIME_MS 10
#define MYSENSOR_REG_ID 0x00
#define MYSENSOR_REG_TEMP 0xFA
#define MYSENSOR_REG_PRESS 0xF7
#define MYSENSOR_REG_HUMIDITY 0xFD

struct mysensor_config {
    struct i2c_dt_spec i2c;
};

struct mysensor_data {
    uint8_t chip_id;
    int16_t temp_raw;

    int32_t raw_humidity;
    int32_t raw_temperature;
    int32_t raw_pressure;
    
};

#endif /* ZEPHYR_DRIVERS_SENSOR_MYSENSOR_MYSENSOR_H_ */
