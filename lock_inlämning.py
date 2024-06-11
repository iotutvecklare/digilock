from machine import Pin, PWM
import time

# Definiera pins för knappar och LEDs
button_pins = [16, 17, 18]
led_red_pin = 19
led_green_pin = 21
prog_button_pin = 23
servo_pin = 22

# Initiera servo och PWM
servo = PWM(Pin(servo_pin), freq=50)

# settings för debounce
debounce_time = 50

# Standardkombinationen (kan ändras)
combination = [1, 2, 3, 4]
input_buffer = [0, 0, 0, 0]
input_index = 0

# Variabler för debounce
last_press_time = [0, 0, 0]
last_button_state = [1, 1, 1]

# Initiera pins
buttons = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in button_pins]
led_red = Pin(led_red_pin, Pin.OUT)
led_green = Pin(led_green_pin, Pin.OUT)
prog_button = Pin(prog_button_pin, Pin.IN, Pin.PULL_UP)


def lock():
    """Låser låset genom att tända röd LED och stänga servon."""
    set_led_state(led_red, True)
    set_led_state(led_green, False)
    servo.duty(40)


def unlock():
    """Låser upp låset genom att tända grön LED och öppna servon."""
    set_led_state(led_red, False)
    set_led_state(led_green, True)
    servo.duty(115)


def set_led_state(led, state):
    """Ställer in LED state."""
    led.value(1 if state else 0)


def debounce_button(index):
    """Debounce för knapptryckning."""
    current_time = time.ticks_ms()
    if current_time - last_press_time[index] > debounce_time:
        last_press_time[index] = current_time
        return True
    return False


def update_input_buffer(button_index):
    """Uppdaterar inputbufferten med senaste knapptryckningen."""
    global input_index
    input_buffer[input_index] = button_index + 1
    input_index = (input_index + 1) % len(input_buffer)


def check_combination():
    """Kontrollerar om inputen matchar den korrekta kombinationen."""
    return input_buffer == combination


def main_loop():
    """mainloop """
    global last_button_state

    while True:
        for i, button in enumerate(buttons):
            button_state = button.value()
            if button_state == 0 and last_button_state[i] == 1:
                if debounce_button(i):
                    update_input_buffer(i)
                    if check_combination():
                        unlock()
                    else:
                        lock()
            last_button_state[i] = button_state

        # kontrollerar om programmeringsknappen är intryckt om den är = kör set_new_combination()
        if prog_button.value() == 0:
            set_new_combination()
        time.sleep_ms(10)


def set_new_combination():
    """Ställer in en ny kombination genom att läsa knapptryckningar och kräver bekräftelse."""
    global combination, input_index
    print("Ställer in ny kombination...")
    new_combination = [0] * len(combination)

    # Läs in den nya kombinationen
    for i in range(len(new_combination)):
        while True:
            for j, button in enumerate(buttons):
                if button.value() == 0 and last_button_state[j] == 1:
                    if debounce_button(j):
                        new_combination[i] = j + 1
                        time.sleep(0.5)  # sleep för att förhindra att knappen trycks ner fler gånger än menat
                        print(f"Satt ny kombination index {i} till {new_combination[i]}")
                        break
            else:
                continue
            break

    print("Bekräfta den nya kombinationen...")
    confirmation_combination = [0] * len(combination)

    # läs in bekräftelsekombon
    for i in range(len(confirmation_combination)):
        while True:
            for j, button in enumerate(buttons):
                if button.value() == 0 and last_button_state[j] == 1:
                    if debounce_button(j):
                        confirmation_combination[i] = j + 1
                        time.sleep(0.5)  # # sleep för att förhindra att knappen trycks ner fler gånger än menat 
                        print(f"Satt bekräftelsekombination index {i} till {confirmation_combination[i]}")
                        break
            else:
                continue
            break

    # kontrollerar bekräftelsekombon igen
    if new_combination == confirmation_combination:
        combination = new_combination
        print("Ny kombination inställd!")
    else:
        print("Bekräftelse misslyckades. Försök igen.")


# start mainloop
main_loop()