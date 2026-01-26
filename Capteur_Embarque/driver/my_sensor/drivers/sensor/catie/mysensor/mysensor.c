/*
 * Copyright (c) 2025, CATIE
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT catie_mysensor

#include <zephyr/drivers/sensor.h>
#include <zephyr/logging/log.h>

#include "mysensor.h"

LOG_MODULE_REGISTER(MYSENSOR, CONFIG_SENSOR_LOG_LEVEL);

static inline int mysensor_bus_check(const struct device *dev){
	const struct mysensor_config *config = dev->config;

	return device_is_ready(config->i2c.bus) ? 0 : -ENODEV;
}

static int mysensor_reg_read(const struct device *dev, uint8_t start, uint8_t *buf, int size){
	const struct mysensor_config *config = dev->config;

	return i2c_burst_read_dt(&config->i2c, start, buf, size);
}

static int mysensor_reg_write(const struct device *dev, uint8_t reg, uint8_t val){
	const struct mysensor_config *config = dev->config;

	return i2c_reg_write_byte_dt(&config->i2c, reg, val);
}

static int mysensor_attr_set(const struct device *dev, enum sensor_channel chan,
			      enum sensor_attribute attr, const struct sensor_value *val)
{
	printk("mysensor_attr_set called");
	return -ENOTSUP;
}

static int mysensor_sample_fetch(const struct device *dev, enum sensor_channel chan)
{
        struct mysensor_data *data = dev->data;
        uint8_t buf[3];
        int err;

        ARG_UNUSED(chan);

        err = mysensor_reg_read(dev, MYSENSOR_REG_PRESS, buf, 3);
        if (err) {
                return err;
        }
        data->raw_pressure =
                ((int32_t)buf[0] << 12) |
                ((int32_t)buf[1] << 4) |
                ((int32_t)buf[2] >> 4);

        err = mysensor_reg_read(dev, MYSENSOR_REG_TEMP, buf, 3);
        if (err) {
                return err;
        }
        data->raw_temperature =
                ((int32_t)buf[0] << 12) |
                ((int32_t)buf[1] << 4) |
                ((int32_t)buf[2] >> 4);

        err = mysensor_reg_read(dev, MYSENSOR_REG_HUMIDITY, buf, 2);
        if (err) {
                return err;
        }
        data->raw_humidity =
                ((int32_t)buf[0] << 8) | buf[1];

        return 0;
}

static int mysensor_channel_get(const struct device *dev, enum sensor_channel chan,
                                 struct sensor_value *val)
{
        struct mysensor_data *data = dev->data;

        switch(chan){

        case SENSOR_CHAN_AMBIENT_TEMP:
                val->val1 = (int32_t)((float)data->raw_temperature * 125.0f / 1048576.0f)-40.0f;
                val->val2 = 0;
                break;
        case SENSOR_CHAN_PRESS:
                val->val1 = (int32_t)(300.0f + ((float)data->raw_pressure * 800.0f / 1048576.0f));
                val->val2 = 0;
                break;
        case SENSOR_CHAN_HUMIDITY:
                val->val1 = data->raw_humidity * 100 / 65535;
                val->val2 = 0;
                break;

        default:
                return -ENOTSUP;
        }
        return 0;
}

static int mysensor_init(const struct device *dev)
{
        struct mysensor_data *data = dev->data;
        int err;

        err = mysensor_bus_check(dev);
        if (err < 0) {
                return err;
        }

        k_msleep(MYSENSOR_START_UP_TIME_MS);

        err = mysensor_reg_read(dev, MYSENSOR_REG_ID, &data->chip_id, 1);
        if (err < 0) {
                return err;
        }

        return 0;
}


static DEVICE_API(sensor, mysensor_driver_api) = {
	.attr_set = mysensor_attr_set,
	.sample_fetch = mysensor_sample_fetch,
	.channel_get = mysensor_channel_get,
};

#define MYSENSOR_INIT(n)                                                     \
    static const struct mysensor_config mysensor_config_##n = {              \
        .i2c = I2C_DT_SPEC_INST_GET(n)                                       \
    };                                                                       \
    static struct mysensor_data mysensor_data_##n;                           \
    SENSOR_DEVICE_DT_INST_DEFINE(n, mysensor_init, NULL,                     \
        &mysensor_data_##n, &mysensor_config_##n,                             \
        POST_KERNEL, CONFIG_SENSOR_INIT_PRIORITY, &mysensor_driver_api);


DT_INST_FOREACH_STATUS_OKAY(MYSENSOR_INIT)
