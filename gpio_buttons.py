import time
from threading import Thread
from db import log_event  

# button pins
IN_BUTTON_PIN = 17
OUT_BUTTON_PIN = 27

# saving current num of people
people = []

def handle_in_button():
    people.append(time.time())
    log_event("IN (physical)")
    print("[GPIO] IN button pressed")

def handle_out_button():
    if people:
        people.pop(0)
    log_event("OUT (physical)")
    print("[GPIO] OUT button pressed")

def listen_buttons():
    print("[GPIO] Listening for button presses...")

    try:
        import RPi.GPIO as GPIO
    except ImportError:
        print("RPi.GPIO not available — running outside Raspberry Pi")
        return

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IN_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(OUT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    while True:
        if GPIO.input(IN_BUTTON_PIN) == GPIO.LOW:
            handle_in_button()
            time.sleep(0.5)
        if GPIO.input(OUT_BUTTON_PIN) == GPIO.LOW:
            handle_out_button()
            time.sleep(0.5)

def start_gpio_listener():
    Thread(target=listen_buttons, daemon=True).start()