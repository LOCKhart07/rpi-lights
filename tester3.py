import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# BCM GPIOs that are generally safe to toggle
SAFE_BCM_PINS = [
    21,  # GPIO21 (pin 40)
    20,  # GPIO20 (pin 38)
    16,  # GPIO16 (pin 36)
    12,  # GPIO12 (pin 32)
    26,  # GPIO26 (pin 37)
    19,  # GPIO19 (pin 35)
    13,  # GPIO13 (pin 33)
    6,   # GPIO6  (pin 31)
    5,   # GPIO5  (pin 29)
]

# Setup
for pin in SAFE_BCM_PINS:
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

try:
    while True:
        for pin in SAFE_BCM_PINS:
            print(pin)
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
