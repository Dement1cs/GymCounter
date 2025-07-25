# Documentation on physical buttons (gpio_buttons.py)

All code for working with physical buttons is moved to the `gpio_buttons.py`.

## File structure

- **pins**  
    ```python
    IN_BUTTON_PIN = 17   # GPIO-pin for «IN»
    OUT_BUTTON_PIN = 27  # GPIO-pin for «OUT»
    ```
# Handler functions
    ```python
    def handle_in_button():
        people.append(time.time())
        log_event("IN (physical)")
        print("[GPIO] IN button pressed")

    def handle_out_button():
        if people:
            people.pop(0)
        log_event("OUT (physical)")
        print("[GPIO] OUT button pressed")
    ```

# Listener
    ```python
    def listen_buttons():
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
    ```

# Entry point
    ```python
    def start_gpio_listener():
    Thread(target=listen_buttons, daemon=True).start()
    ```

## How to connect

# Make sure the library is installed on the Pi:

    ```python
    sudo apt install python3-rpi.gpio
    ```
    
# The buttons are connected like this:

    ```python
    One contact of the button is to the GPIO pin (17 or 27).
    The second is to GND (when using pull_up_down=GPIO.PUD_UP).
    ```

# In app.py, import and start the listener:

    ```python
    from gpio_buttons import start_gpio_listener, people
    ...
    start_gpio_listener()
    ```