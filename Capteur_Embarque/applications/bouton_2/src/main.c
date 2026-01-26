/*
 * Copyright (c) 2016 Open-RnD Sp. z o.o.
 * Copyright (c) 2020 Nordic Semiconductor ASA
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/sys/util.h>
#include <zephyr/sys/printk.h>
#include <inttypes.h>

/* Configuration du bouton */
#define SW0_NODE DT_ALIAS(sw0)
#if !DT_NODE_HAS_STATUS_OKAY(SW0_NODE)
#error "Unsupported board: sw0 devicetree alias is not defined"
#endif
static const struct gpio_dt_spec button = GPIO_DT_SPEC_GET_OR(SW0_NODE, gpios, {0});
static struct gpio_callback button_cb_data;

/* Configuration de la LED */
static struct gpio_dt_spec led = GPIO_DT_SPEC_GET_OR(DT_ALIAS(led0), gpios, {0});

/* Variables pour le clignotement */
static uint32_t blink_interval_ms = 5000;     /* Période initiale : 5 s */
static const uint32_t MIN_INTERVAL_MS = 100;  /* Limite minimale : 0.1 s */
static const uint32_t MAX_INTERVAL_MS = 5000; /* Limite maximale : 5 s */
static const float SPEED_FACTOR = 0.5;        /* Divise la période par 2 à chaque appui */

/* Callback appelée lors d’un appui sur le bouton */
void button_pressed(const struct device *dev, struct gpio_callback *cb, uint32_t pins)
{
    ARG_UNUSED(dev);
    ARG_UNUSED(cb);
    ARG_UNUSED(pins);

    /* Réduction de la période (accélération) */
    blink_interval_ms = (uint32_t)((float)blink_interval_ms * SPEED_FACTOR);

    /* Si on atteint la limite, on repart à 5 s */
    if (blink_interval_ms < MIN_INTERVAL_MS) {
        blink_interval_ms = MAX_INTERVAL_MS;
    }

    printk("Button pressed -> blink interval: %u ms\n", blink_interval_ms);
}

int main(void)
{
    int ret;

    /* Vérifie que le bouton est prêt */
    if (!gpio_is_ready_dt(&button)) {
        printk("Error: button device %s is not ready\n", button.port->name);
        return 0;
    }

    ret = gpio_pin_configure_dt(&button, GPIO_INPUT);
    if (ret != 0) {
        printk("Error %d: failed to configure %s pin %d\n", ret, button.port->name, button.pin);
        return 0;
    }

    /* Interruption sur front montant */
    ret = gpio_pin_interrupt_configure_dt(&button, GPIO_INT_EDGE_TO_ACTIVE);
    if (ret != 0) {
        printk("Error %d: failed to configure interrupt on %s pin %d\n",
               ret, button.port->name, button.pin);
        return 0;
    }

    /* Enregistre la callback du bouton */
    gpio_init_callback(&button_cb_data, button_pressed, BIT(button.pin));
    gpio_add_callback(button.port, &button_cb_data);
    printk("Set up button at %s pin %d\n", button.port->name, button.pin);

    /* Configure la LED */
    if (led.port && !gpio_is_ready_dt(&led)) {
        printk("Error: LED device %s is not ready\n", led.port->name);
        led.port = NULL;
    }

    if (led.port) {
        ret = gpio_pin_configure_dt(&led, GPIO_OUTPUT_INACTIVE);
        if (ret != 0) {
            printk("Error %d: failed to configure LED device %s pin %d\n",
                   ret, led.port->name, led.pin);
            led.port = NULL;
        } else {
            printk("Set up LED at %s pin %d\n", led.port->name, led.pin);
        }
    }

    printk("Press the button to accelerate LED blinking\n");

    bool led_state = false;

    /* Boucle principale : clignotement de la LED */
    while (1) {
        if (led.port) {
            led_state = !led_state;
            gpio_pin_set_dt(&led, led_state);
        }
        k_msleep(blink_interval_ms);
    }

    return 0;
}
