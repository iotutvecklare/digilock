import machine
import time
import os

# Constants
DEBOUNCE_DELAY = 50  # Debounce delay in milliseconds

# Pins
RED_LED_PIN = 7 # D4
GREEN_LED_PIN = 6 # D3
BUTTON_PINS = [9, 10, 17, 18]
RESET_PIN = 8
SERVO_PIN = 5

# Define the correct passcode sequence
passcode = [1, 4, 2, 2]
buffer_code = [0, 0, 0, 0]
buffer = 0
reset_trigger = 0

# Debounce variables
last_debounce_times = [0, 0, 0, 0, 0]
button_states = [0, 0, 0, 0, 0]
last_button_states = [1, 1, 1, 1, 1]

# Initialize LEDs, buttons, and servo
red_led = machine.Pin(RED_LED_PIN, machine.Pin.OUT)
green_led = machine.Pin(GREEN_LED_PIN, machine.Pin.OUT)
buttons = [machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP) for pin in BUTTON_PINS]
reset_button = machine.Pin(RESET_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
#servo = machine.PWM(machine.Pin(SERVO_PIN), freq=50)
servo = machine.PWM(machine.Pin(SERVO_PIN, mode=machine.Pin.OUT))  
servo.freq(50) 

"""
Let's say buffer_code initially is [2, 4, 1, 3] and buffer is 4.
1. Initial State:
    buffer_code = [5, 6, 7, 8]
    buffer = 9
    
2. After Loop:
    buffer_code[0] = buffer_code[1] → buffer_code = [4, 4, 1, 3]
    buffer_code[1] = buffer_code[2] → buffer_code = [4, 1, 1, 3]
    buffer_code[2] = buffer_code[3] → buffer_code = [4, 1, 3, 3]
    
3. Assign New Value:
    buffer_code[3] = buffer → buffer_code = [4, 1, 3, 4]

4. Reset buffer:
    buffer = 0
    
"""
def swap():
    global buffer_code, buffer
    for i in range(3):
        buffer_code[i] = buffer_code[i + 1]
    buffer_code[3] = buffer
    buffer = 0

def check_buttons():
    global buffer
    current_time = time.ticks_ms()

    for i in range(4):
        reading = buttons[i].value()
        if reading != last_button_states[i]:
            last_debounce_times[i] = current_time
            last_button_states[i] = reading
        elif (current_time - last_debounce_times[i]) > DEBOUNCE_DELAY:
            if reading != button_states[i]:
                button_states[i] = reading
                if button_states[i] == 0:
                    buffer = i + 1
                    print(f"Button {i + 1} pressed")
                    swap()
                    check_passcode()
                    
                    
    reset_password(current_time)                

def reset_password(current_time):
    global reset_trigger
    reading_reset = reset_button.value()
    if reading_reset != last_button_states[4]:
        last_debounce_times[4] = current_time
        last_button_states[4] = reading_reset
    elif (current_time - last_debounce_times[4]) > DEBOUNCE_DELAY:
        if reading_reset != button_states[4]:
            button_states[4] = reading_reset
            if button_states[4] == 0:
                if reset_trigger == 0:
                    reset_trigger = 1
                    print("Reset passcode. Please enter 4 new numbers")
                    print("and then press the reset button again to save new passcode")
                elif reset_trigger == 1:
                    for i in range(4):
                        passcode[i] = buffer_code[i]
                        buffer_code[i] = 0
                    reset_trigger = 0
                    print("Passcode has been changed")
                    write_to_file()

def check_passcode():
    global buffer_code
    if buffer_code == passcode:
        red_led.value(0)
        green_led.value(1)
        servo.duty(45)
        print("Unlocked!")
        time.sleep(5) 
        green_led.value(0) 
        for i in range(4):
            buffer_code[i] = 0
        print("Locked!")
        servo.duty(90) 
        red_led.value(1) 
        

def write_to_file():
    global passcode
    with open('data.txt', 'w') as f:
        f.write(' '.join(map(str, passcode)))
    print("Passcode saved")
    

def read_from_file():
    with open('data.txt', 'r') as file:
        # Use strip() to remove any trailing newline characters
        data_from_file = file.readline().strip()
    return data_from_file        


red_led.value(1)  # Red LED ON
servo.duty(90)  # Close servo

if 'data.txt' in os.listdir():
    passcode = read_from_file()
    passcode = [int(num) for num in passcode.split()]

while True:
    check_buttons()
    time.sleep(0.1)  # Sleep for 100 ms to avoid high CPU usage
