#!/usr/bin/env python3

import time
import signal
import sys
import RPi.GPIO as GPIO

BUTTON_PIN = 18  # BCM

def cleanup(sig=None, frame=None):
    print("\nCleaning up GPIO, exiting.")
    GPIO.cleanup()
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    print("Ready.")
    print(f"Short GPIO {BUTTON_PIN} to GND to trigger.")
    print("Ctrl+C to exit.\n")

    last_state = GPIO.input(BUTTON_PIN)

    while True:
        state = GPIO.input(BUTTON_PIN)

        # Detect HIGH -> LOW transition
        if last_state == GPIO.HIGH and state == GPIO.LOW:
            print(f"[EVENT] Button pressed on GPIO {BUTTON_PIN}")

        last_state = state
        time.sleep(0.01)  # 10 ms polling (instant for humans)

if __name__ == "__main__":
    main()
