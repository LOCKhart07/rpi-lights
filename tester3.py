import time

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

PINS = [
    6,
    # 13,
    19,
    26,
    5,
    16,
    # # 21,  # pin 40
    # # 20,  # pin 38
    # # 16,  # pin 36
    # # 5,  # pin 29
    # # 26,  # pin 37
    # 19,
    # 13,
]

# ---- STARTUP STATE ----
# LOW = relay energized → NC open → lights OFF
for pin in PINS:
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

print("Startup: all lights OFF")

try:
    while True:
        for pin in PINS:
            print(f"Toggling pin {pin}")

            # Turn ON light
            GPIO.output(pin, GPIO.HIGH)  # relay off → NC closed
            time.sleep(1)

            # Turn OFF light
            GPIO.output(pin, GPIO.LOW)  # relay on → NC open
            time.sleep(1)

except KeyboardInterrupt:
    print("Stopping — lights will turn ON (fail-safe)")

finally:
    # FAIL-SAFE: release GPIO so relays drop out
    for pin in PINS:
        GPIO.setup(pin, GPIO.IN)

    GPIO.cleanup()
