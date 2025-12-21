#!/usr/bin/env python3

import signal
import subprocess
import sys
import time

import RPi.GPIO as GPIO

# from EmulatorGUI import GPIO

# ===================== CONFIG =====================

# GPIO pins connected to relay IN pins (BCM numbering)
RELAY_PINS = [17, 27, 22]

# True if your relay board turns ON when GPIO is LOW
ACTIVE_LOW = True

# Audio file (WAV recommended for accurate timing)
AUDIO_FILE = "monologue.wav"


LIGHT_1_PIN = 21  # GPIO21 (pin 40)
LIGHT_2_PIN = 20  # GPIO20 (pin 38)
LIGHT_3_PIN = 16  # GPIO16 (pin 36)
LIGHT_4_PIN = 12  # GPIO12 (pin 32)
LIGHT_5_PIN = 26  # GPIO26 (pin 37)
LIGHT_6_PIN = 19  # GPIO19 (pin 35)
LIGHT_7_PIN = 13  # GPIO13 (pin 33)
LIGHT_8_PIN = 6  # GPIO6  (pin 31)

# Cue format:
# (time_in_seconds_from_start, gpio_pin, state)
# state: True = ON, False = OFF
CUES = [
    (0.0, LIGHT_1_PIN, True),  # Light 1 ON immediately
    (1.0, LIGHT_1_PIN, False),  # Light 1 OFF
    (1.1, LIGHT_2_PIN, True),  # Light 2 ON
    (2.0, LIGHT_2_PIN, False),  # Light 2 OFF
    (2.1, LIGHT_3_PIN, True),  # Light 3 ON
    (3.0, LIGHT_3_PIN, False),  # Light 3 OFF
    (3.1, LIGHT_4_PIN, True),  # Light 4 ON
    (4.0, LIGHT_4_PIN, False),  # Light 4 OFF
    (4.1, LIGHT_5_PIN, True),  # Light 5 ON
    (5.0, LIGHT_5_PIN, False),  # Light 5 OFF
    (5.1, LIGHT_6_PIN, True),  # Light 6 ON
    (6.0, LIGHT_6_PIN, False),  # Light 6 OFF
    (6.1, LIGHT_7_PIN, True),  # Light 7 ON
    (7.0, LIGHT_7_PIN, False),  # Light 7 OFF
    (7.1, LIGHT_8_PIN, True),  # Light 8 ON
    (8.0, LIGHT_8_PIN, False),  # Light 8 OFF
]

# ================================================


def relay_on(pin):
    GPIO.output(pin, GPIO.LOW if ACTIVE_LOW else GPIO.HIGH)


def relay_off(pin):
    GPIO.output(pin, GPIO.HIGH if ACTIVE_LOW else GPIO.LOW)


def cleanup_and_exit(*_):
    print("\nCleaning up GPIO...")
    for pin in RELAY_PINS:
        relay_off(pin)
    GPIO.cleanup()
    sys.exit(0)


def main():
    # Handle Ctrl+C cleanly
    signal.signal(signal.SIGINT, cleanup_and_exit)
    signal.signal(signal.SIGTERM, cleanup_and_exit)

    # GPIO setup
    GPIO.setmode(GPIO.BCM)
    for pin in RELAY_PINS:
        GPIO.setup(pin, GPIO.OUT)
        relay_off(pin)

    print("Starting monologue + light sync")

    # Start audio playback (non-blocking)
    # subprocess.Popen(["aplay", AUDIO_FILE])

    start_time = time.monotonic()

    # Execute cues
    for cue_time, pin, state in CUES:
        # Busy-wait until the exact cue time
        while time.monotonic() - start_time < cue_time:
            time.sleep(0.001)

        if state:
            relay_on(pin)
            action = "ON"
        else:
            relay_off(pin)
            action = "OFF"

        print(f"{cue_time:6.2f}s | GPIO {pin} → {action}")

    print("All cues completed")

    # Keep script alive until audio finishes (optional)
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
