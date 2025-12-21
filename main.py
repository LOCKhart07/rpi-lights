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

# Cue format:
# (time_in_seconds_from_start, gpio_pin, state)
# state: True = ON, False = OFF
CUES = [
    (0.0, 17, True),  # Light 1 ON immediately
    (4.5, 17, False),  # Light 1 OFF
    (4.5, 27, True),  # Light 2 ON
    (9.8, 27, False),  # Light 2 OFF
    (10.0, 22, True),  # Light 3 ON
    (18.0, 22, False),  # Light 3 OFF
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
