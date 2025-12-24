#!/usr/bin/env python3

import signal
import subprocess
import sys
import time
from datetime import datetime

import RPi.GPIO as GPIO

# from EmulatorGUI import GPIO


# ===================== CONFIG =====================

# True if your relay board turns ON when GPIO is LOW
ACTIVE_LOW = True

# Audio file (WAV recommended for accurate timing)
AUDIO_FILE = "actual_monologue.wav"

# Global audio process handle
audio_proc = None


LIGHT_1_PIN = 21  # GPIO21 (pin 40)
LIGHT_2_PIN = 20  # GPIO20 (pin 38)
LIGHT_3_PIN = 16  # GPIO16 (pin 36)
# LIGHT_4_PIN = 12  # GPIO12 (pin 32)
LIGHT_4_PIN = 5  # GPIO5 (pin 29)
LIGHT_5_PIN = 26  # GPIO26 (pin 37)
LIGHT_6_PIN = 19  # GPIO19 (pin 35)
LIGHT_7_PIN = 13  # GPIO13 (pin 33)
LIGHT_8_PIN = 6  # GPIO6  (pin 31)

# GPIO pins connected to relay IN pins (BCM numbering)
RELAY_PINS = [
    LIGHT_1_PIN,
    LIGHT_2_PIN,
    LIGHT_3_PIN,
    LIGHT_4_PIN,
    LIGHT_5_PIN,
    # LIGHT_6_PIN,
    # LIGHT_7_PIN,
    # LIGHT_8_PIN,
]

# Cue format:
# (time_in_seconds_from_start, gpio_pin, state)
# state: True = ON, False = OFF
CUES = [
    (0.0, LIGHT_1_PIN, True),  # Light 1 ON at 0:00
    (47, LIGHT_1_PIN, False),  # Light 1 OFF at 0:47
    (48, LIGHT_2_PIN, True),  # Light 2 ON at 0:48
    (97, LIGHT_2_PIN, False),  # Light 2 OFF at 1:37
    (98, LIGHT_3_PIN, True),  # Light 3 ON at 1:38
    (172, LIGHT_3_PIN, False),  # Light 3 OFF at 2:52
    (173, LIGHT_4_PIN, True),  # Light 4 ON at 2:53
    (221, LIGHT_4_PIN, False),  # Light 4 OFF at 3:41
    (222, LIGHT_5_PIN, True),  # Light 5 ON at 3:42
    (331, LIGHT_5_PIN, False),  # Light 5 OFF at 5:31
    # (7.7, LIGHT_6_PIN, True),  # Light 6 ON
    # (9.15, LIGHT_6_PIN, False),  # Light 6 OFF
    # (9.15, LIGHT_7_PIN, True),  # Light 7 ON
    # (10.71, LIGHT_7_PIN, False),  # Light 7 OFF
    # (10.71, LIGHT_8_PIN, True),  # Light 8 ON
    # (12.14, LIGHT_8_PIN, False),  # Light 8 OFF
]

# ================================================


def relay_on(pin):
    GPIO.output(pin, GPIO.LOW if ACTIVE_LOW else GPIO.HIGH)


def relay_off(pin):
    GPIO.output(pin, GPIO.HIGH if ACTIVE_LOW else GPIO.LOW)


def stop_audio():
    # Stop audio if playing
    if audio_proc and audio_proc.poll() is None:
        print("Stopping audio...")
        audio_proc.terminate()
        try:
            audio_proc.wait(timeout=1)
        except subprocess.TimeoutExpired:
            audio_proc.kill()


def cleanup_and_exit(*_):
    print("\nCleaning up GPIO...")
    for pin in RELAY_PINS:
        relay_off(pin)
    GPIO.cleanup()
    stop_audio()
    print("Exiting.")
    sys.exit(0)


def turn_everything_on():
    print("Turning everything ON")
    for pin in RELAY_PINS:
        relay_on(pin)


def turn_everything_off():
    print("Turning everything OFF")
    for pin in RELAY_PINS:
        relay_off(pin)


def is_daytime():
    """Check if current time is between 1:30 AM and 6:00 PM"""
    now = datetime.now()
    current_time = now.time()
    start_time = datetime.strptime("01:30", "%H:%M").time()
    end_time = datetime.strptime("18:00", "%H:%M").time()
    return start_time <= current_time <= end_time


def main():
    # Handle Ctrl+C cleanly
    signal.signal(signal.SIGINT, cleanup_and_exit)
    signal.signal(signal.SIGTERM, cleanup_and_exit)

    # GPIO setup
    GPIO.setmode(GPIO.BCM)
    for pin in RELAY_PINS:
        GPIO.setup(pin, GPIO.OUT)
        relay_off(pin)

    turn_everything_on()
    time.sleep(5)
    turn_everything_off()

    while True:
        if is_daytime():
            print("Daytime mode (1:30 AM - 6:00 PM): Lights staying on")
            turn_everything_on()
            time.sleep(60)  # Check every minute
        else:
            turn_everything_off()
            time.sleep(1)
            execute_light_audio_cues()
            turn_everything_on()
            time.sleep(30)
            turn_everything_off()
            time.sleep(3)


def execute_light_audio_cues():
    print("Starting monologue + light sync")

    for pin in RELAY_PINS:
        relay_off(pin)

    # Start audio playback (non-blocking)
    global audio_proc
    audio_proc = subprocess.Popen(
        ["aplay", AUDIO_FILE],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

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
    print("waiting for audio to finish...")
    audio_proc.wait()
    print("Audio finished.")


if __name__ == "__main__":
    main()
