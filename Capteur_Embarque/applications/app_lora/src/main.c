/*
 * Class A LoRaWAN sample application
 *
 * Copyright (c) 2020 Manivannan Sadhasivam <mani@kernel.org>
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/device.h>
#include <zephyr/lorawan/lorawan.h>
#include <zephyr/kernel.h>

#include <zephyr/drivers/sensor.h>

#include <zephyr/drivers/flash.h>
#include <zephyr/storage/flash_map.h>
#include <zephyr/fs/nvs.h>

#include <stdio.h>

/* Customize based on network configuration */
#define LORAWAN_DEV_EUI			{ 0xFE, 0xFF, 0xFF, 0xFF, 0xFD, 0xFF,\
					  0x00, 0x09 }
#define LORAWAN_JOIN_EUI		{ 0xFE, 0xFF, 0xFF, 0xFF, 0xFD, 0xFF,\
					  0xC0, 0xDE }
#define LORAWAN_APP_KEY			{ 0xBF, 0x7C, 0xE9, 0x6F, 0xEE, 0x3F,\
					  0xEB, 0xC2, 0xB6, 0x30, 0x8A, 0x97,\
					  0xDD, 0x07, 0xE7, 0xF0 }

#define DELAY K_MSEC(10000)

#define LOG_LEVEL CONFIG_LOG_DEFAULT_LEVEL
#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(lorawan_class_a);

char data[100];

static struct nvs_fs fs;

#define NVS_PARTITION storage_partition
#define NVS_PARTITION_DEVICE FIXED_PARTITION_DEVICE(NVS_PARTITION)
#define NVS_PARTITION_OFFSET FIXED_PARTITION_OFFSET(NVS_PARTITION)

#define NVS_DEVNONCE_ID 10

static int nvs_init(void)
{
	int rc;
	struct flash_pages_info info;

	fs.flash_device = NVS_PARTITION_DEVICE;
	if (!device_is_ready(fs.flash_device)) {
		LOG_ERR("Flash device %s is not ready", fs.flash_device->name);
		return -ENODEV;
	}

	fs.offset = NVS_PARTITION_OFFSET;

	rc = flash_get_page_info_by_offs(fs.flash_device, fs.offset, &info);
	if (rc) {
		LOG_ERR("Unable to get page info, rc=%d", rc);
		return rc;
	}

	fs.sector_size = info.size;
	fs.sector_count = 3U;

	rc = nvs_mount(&fs);
	if (rc) {
		LOG_ERR("Flash Init failed, rc=%d", rc);
		return rc;
	}

	return 0;
}

static int nvs_load_dev_nonce(uint16_t *dev_nonce)
{
	LOG_INF("test");
	int rc = nvs_read(&fs, NVS_DEVNONCE_ID, dev_nonce, sizeof(*dev_nonce));

	LOG_INF("%d", rc);
	LOG_INF("%d", dev_nonce);

	*dev_nonce = 7;
	rc = nvs_write(&fs, NVS_DEVNONCE_ID, dev_nonce, sizeof(*dev_nonce));
	if (rc < 0) {
		return rc;
	}

	return 0;
}

static int nvs_store_dev_nonce(uint16_t dev_nonce)
{
	return nvs_write(&fs, NVS_DEVNONCE_ID, &dev_nonce, sizeof(dev_nonce));
}

static void dl_callback(uint8_t port, uint8_t flags, int16_t rssi, int8_t snr, uint8_t len,
			const uint8_t *hex_data)
{
	LOG_INF("Port %d, Pending %d, RSSI %ddB, SNR %ddBm, Time %d", port,
		flags & LORAWAN_DATA_PENDING, rssi, snr, !!(flags & LORAWAN_TIME_UPDATED));
	if (hex_data) {
		LOG_HEXDUMP_INF(hex_data, len, "Payload: ");
	}
}

static void lorwan_datarate_changed(enum lorawan_datarate dr)
{
	uint8_t unused, max_size;

	lorawan_get_payload_sizes(&unused, &max_size);
	LOG_INF("New Datarate: DR_%d, Max Payload %d", dr, max_size);
}

int main(void)
{
	const struct device *lora_dev;
	const struct device *const dev = DEVICE_DT_GET(DT_NODELABEL(mysensor));
	struct lorawan_join_config join_cfg;
	struct sensor_value temp_val, press_val, hum_val;
	uint8_t dev_eui[] = LORAWAN_DEV_EUI;
	uint8_t join_eui[] = LORAWAN_JOIN_EUI;
	uint8_t app_key[] = LORAWAN_APP_KEY;
	int ret;
	int err;

	uint16_t dev_nonce;

	struct lorawan_downlink_cb downlink_cb = {
		.port = LW_RECV_PORT_ANY,
		.cb = dl_callback
	};

	lora_dev = DEVICE_DT_GET(DT_ALIAS(lora0));
	if (!device_is_ready(lora_dev)) {
		LOG_ERR("%s: device not ready.", lora_dev->name);
		return 0;
	}

	if (!device_is_ready(dev)) {
		printk("Device %s is not ready\n", dev->name);
		return 1;
	}

	ret = nvs_init();
	if (ret < 0) {
		return 0;
	}

	ret = nvs_load_dev_nonce(&dev_nonce);
	if (ret < 0) {
		return 0;
	}

	k_sleep(K_MSEC(1000));

#if defined(CONFIG_LORAMAC_REGION_EU868)
	/* If more than one region Kconfig is selected, app should set region
	 * before calling lorawan_start()
	 */
	ret = lorawan_set_region(LORAWAN_REGION_EU868);
	if (ret < 0) {
		LOG_ERR("lorawan_set_region failed: %d", ret);
		return 0;
	}
#endif

	ret = lorawan_start();
	if (ret < 0) {
		LOG_ERR("lorawan_start failed: %d", ret);
		return 0;
	}

	lorawan_register_downlink_callback(&downlink_cb);
	lorawan_register_dr_changed_callback(lorwan_datarate_changed);

	join_cfg.mode = LORAWAN_ACT_OTAA;
	join_cfg.dev_eui = dev_eui;
	join_cfg.otaa.join_eui = join_eui;
	join_cfg.otaa.app_key = app_key;
	join_cfg.otaa.nwk_key = app_key;
	join_cfg.otaa.dev_nonce = dev_nonce;

	LOG_INF("Joining network over OTAA");
	ret = lorawan_join(&join_cfg);
	if (ret < 0) {
		LOG_ERR("lorawan_join_network failed: %d", ret);
		return 0;
	}

	dev_nonce++;
	(void)nvs_store_dev_nonce(dev_nonce);

	LOG_INF("Sending data...");
	while (1) {
		err = sensor_sample_fetch(dev);
		if (err < 0) {
			printk("Could not fetch sample (%d)\n", err);
				return 0;
		}

		if (sensor_channel_get(dev, SENSOR_CHAN_AMBIENT_TEMP, &temp_val)) {
			printk("Could not get sample\n");
			return 0;
		}
				
		if (sensor_channel_get(dev, SENSOR_CHAN_PRESS, &press_val)) {
			printk("Could not get sample\n");
			return 0;
		}
			
		if (sensor_channel_get(dev, SENSOR_CHAN_HUMIDITY, &hum_val)) {
			printk("Could not get sample\n");
			return 0;
		}

		printk("temperature value: %d\n", temp_val.val1);
		printk("pressure value: %d\n", press_val.val1);
		printk("humidity value: %d\n", hum_val.val1); 

		k_sleep(K_MSEC(2000));

		// Construction du JSON compatible avec l'API Adafruit MQTT Groups
		// On utilise \" pour que les guillemets soient inclus dans le texte
		int len = snprintf(data, sizeof(data), 
			"{\"feeds\":{\"t\":%d,\"h\":%d,\"p\":%d}}", 
			temp_val.val1, hum_val.val1, press_val.val1);

		// Envoi via LoRaWAN
		// Note : Le port (2) doit être celui attendu par le forwarder de votre prof
		ret = lorawan_send(2, data, len, LORAWAN_MSG_CONFIRMED);

		//int len = snprintf(data, sizeof(data), "Temp : %d, Humidity : %d, Pressure : %d", temp_val.val1, hum_val.val1, press_val.val1);

		//ret = lorawan_send(2, data, len,
				   //LORAWAN_MSG_CONFIRMED);

		/*
		 * Note: The stack may return -EAGAIN if the provided data
		 * length exceeds the maximum possible one for the region and
		 * datarate. But since we are just sending the same data here,
		 * we'll just continue.
		 */
		if (ret == -EAGAIN) {
			LOG_ERR("lorawan_send failed: %d. Continuing...", ret);
			k_sleep(DELAY);
			continue;
		}

		if (ret < 0) {
			LOG_ERR("lorawan_send failed: %d", ret);
			return 0;
		}

		LOG_INF("Data sent!");
		k_sleep(DELAY);
	}
}
