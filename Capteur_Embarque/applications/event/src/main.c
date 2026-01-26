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

#define STACK_SIZE 1024
#define PRIORITY 5
#define NB_ITERATIONS 100

/* --- Déclaration des sémaphores --- */
K_SEM_DEFINE(sem_ping, 0, 1);
K_SEM_DEFINE(sem_pong, 0, 1);
K_SEM_DEFINE(start_sem, 0, 1);   /* pour attendre le bouton */

/* --- Déclaration des threads --- */
void ping_thread(void *arg1, void *arg2, void *arg3);
void pong_thread(void *arg1, void *arg2, void *arg3);

K_THREAD_STACK_DEFINE(ping_stack_area, STACK_SIZE);
K_THREAD_STACK_DEFINE(pong_stack_area, STACK_SIZE);

struct k_thread ping_thread_data;
struct k_thread pong_thread_data;

/* --- Configuration du bouton --- */
#define SW0_NODE DT_ALIAS(sw0)
#if !DT_NODE_HAS_STATUS_OKAY(SW0_NODE)
#error "Unsupported board: sw0 devicetree alias is not defined"
#endif

static const struct gpio_dt_spec button = GPIO_DT_SPEC_GET_OR(SW0_NODE, gpios, {0});
static struct gpio_callback button_cb_data;

/* --- Callback du bouton --- */
static void button_pressed(const struct device *dev, struct gpio_callback *cb, uint32_t pins)
{
    ARG_UNUSED(dev);
    ARG_UNUSED(cb);
    ARG_UNUSED(pins);

    printk("Bouton pressé ! Lancement du ping-pong.\n");
    k_sem_give(&start_sem);   /* Débloque le thread ping */
}

/* --- Thread PING --- */
void ping_thread(void *arg1, void *arg2, void *arg3)
{
    printk("Ping thread en attente du bouton...\n");
    k_sem_take(&start_sem, K_FOREVER);
    printk("Ping commence !\n");

    k_sem_give(&sem_ping); // Démarre le ping initial

    for (int i = 0; i < NB_ITERATIONS; i++) {
        k_sem_take(&sem_ping, K_FOREVER);
        printk("ping, %d\n", i);
        k_sem_give(&sem_pong);
        k_msleep(10);
    }
}

/* --- Thread PONG --- */
void pong_thread(void *arg1, void *arg2, void *arg3)
{
    for (int i = 0; i < NB_ITERATIONS; i++) {
        k_sem_take(&sem_pong, K_FOREVER);
        printk("pong, %d\n", i);
        k_sem_give(&sem_ping);
        k_msleep(10);
    }
}

/* --- Fonction principale --- */
void main(void)
{
    printk("=== Programme Ping-Pong déclenché par bouton ===\n");

    int ret;

    /* Initialisation du bouton */
    if (!gpio_is_ready_dt(&button)) {
        printk("Erreur : périphérique bouton %s non prêt\n", button.port->name);
        return;
    }

    ret = gpio_pin_configure_dt(&button, GPIO_INPUT);
    if (ret != 0) {
        printk("Erreur %d : configuration du bouton échouée\n", ret);
        return;
    }

    ret = gpio_pin_interrupt_configure_dt(&button, GPIO_INT_EDGE_TO_ACTIVE);
    if (ret != 0) {
        printk("Erreur %d : configuration de l’interruption échouée\n", ret);
        return;
    }

    gpio_init_callback(&button_cb_data, button_pressed, BIT(button.pin));
    gpio_add_callback(button.port, &button_cb_data);

    printk("Bouton configuré sur %s pin %d\n", button.port->name, button.pin);

    /* --- Création des threads --- */
    k_tid_t ping_tid = k_thread_create(
        &ping_thread_data,
        ping_stack_area,
        K_THREAD_STACK_SIZEOF(ping_stack_area),
        ping_thread,
        NULL, NULL, NULL,
        PRIORITY, 0, K_NO_WAIT);

    k_tid_t pong_tid = k_thread_create(
        &pong_thread_data,
        pong_stack_area,
        K_THREAD_STACK_SIZEOF(pong_stack_area),
        pong_thread,
        NULL, NULL, NULL,
        PRIORITY, 0, K_NO_WAIT);

    k_thread_start(ping_tid);
    k_thread_start(pong_tid);
}
