# Kod för att ett lås, där man kan ställa in sin egna kombination och låsa upp det.
# Ska simulera en digitalstyrd låskolv
# LÄS README.txt
from machine import Pin, PWM
import time

# Definiera pins för knappar och led
button_pins = [16, 17, 18]
led_red_pin = 19
led_green_pin = 21
prog_button_pin = 23
servo_pin = 22

# servo and pwm
servo = PWM(Pin(servo_pin), freq=50)

# Debounce-settings
debounce_time = 50

# Standardkombinationen !kan ändras!
combination = [1, 2, 3, 4]
input_buffer = [0, 0, 0, 0]
input_index = 0

# debounce
last_press_time = [0, 0, 0]
last_button_state = [1, 1, 1]

# Initialise
buttons = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in button_pins]
led_red = Pin(led_red_pin, Pin.OUT)
led_green = Pin(led_green_pin, Pin.OUT)
prog_button = Pin(prog_button_pin, Pin.IN, Pin.PULL_UP)

# Funktion för att låsa låset där det tänds en röd LED och servon stängs
def lock():
    led_red.value(1)
    led_green.value(0)
    servo.duty(40)

# Funktion för att låsa upp låset där det tänds en grön LED och servon öppnas
def unlock():
    led_red.value(0)
    led_green.value(1)
    servo.duty(115)
    time.sleep(5)
    lock()

# Funktion för att hantera knapptryckningar och kontrollera kombination
def handle_button_press(button):
    global input_index
    input_buffer[input_index] = button
    input_index = (input_index + 1) % 4
    if check_combination():
        unlock()

# Funtkion som kontrollerar om kombinationen är korrekt
def check_combination():
    for i in range(4):
        if input_buffer[i] != combination[i]:
            return False
    return True

# Funktion för att spara kombinationen till en fil
def save_combination_to_file():
    with open('combination.txt', 'w') as f:
        f.write(','.join(map(str, combination)))

# Funktion för att läsa kombination från en fil
def load_combination_from_file():
    global combination
    try:
        with open('combination.txt', 'r') as f:
            comb = f.read().split(',')
            if len(comb) == 4:
                combination = list(map(int, comb))
            else:
                raise ValueError('Invalid combination format')
    except (OSError, ValueError):
        combination = [1, 2, 3, 4]
        save_combination_to_file()

# Funktion för att skapa en ny kombination
def program_new_combination():
    new_combination = [0, 0, 0, 0]
    for i in range(4):
        button_pressed = False
        while not button_pressed:
            for j in range(3):
                if buttons[j].value() == 0:
                    new_combination[i] = j + 1
                    button_pressed = True
                    time.sleep(0.3)
                    break
    for i in range(4):
        combination[i] = new_combination[i]
    save_combination_to_file()

# Funktion för att låsa låset och ladda kombination från fil
def setup():
    lock()
    load_combination_from_file()

# Kör initialiseringsfunktionen
setup()

# mainloop
while True:
    current_time = time.ticks_ms()
    if prog_button.value() == 0:
        program_new_combination()
        time.sleep(0.5)
    for i in range(3):
        reading = buttons[i].value()
        if reading != last_button_state[i]:
            last_press_time[i] = current_time
        if time.ticks_diff(current_time, last_press_time[i]) > debounce_time:
            if reading != last_button_state[i]:
                last_button_state[i] = reading
                if reading == 0:
                    handle_button_press(i + 1)
    time.sleep(0.01)