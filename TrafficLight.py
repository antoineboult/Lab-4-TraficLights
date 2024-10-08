from machine import UART, Pin
import time

# Initializes UART
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

# Initialize LEDs and buttons
green_light = Pin(18, Pin.OUT)
yellow_light = Pin(19, Pin.OUT)
red_light = Pin(20, Pin.OUT)

reset_button = Pin(10, Pin.IN, Pin.PULL_UP)  # SW1
northsouth_sensor = Pin(11, Pin.IN, Pin.PULL_UP)  # SW2 (North/South direction)
eastwest_sensor= Pin(12, Pin.IN, Pin.PULL_UP)  # SW3 (East/West direction)

# Traffic light state variables
state = "RED"
other_road_cars = 0

def traffic_light_system():
    global state, other_road_cars
    # State machine transitions
    if state == "RED":
        red_led.on()
        green_led.off()
        yellow_led.off()
        # Wait for 5 seconds in the red state
        time.sleep(5)
        state = "GREEN_A"
        uart.write('NS_RED')  # Notify other Pico that this light is now red
    
    elif state == "GREEN_A":
        green_led.on()
        red_led.off()
        yellow_led.off()
        # Stay green for 5 seconds
        time.sleep(5)
        if other_road_cars < 5:  # Check if other direction is not too busy
            state = "GREEN_B"
        else:
            state = "YELLOW"
    
    elif state == "GREEN_B":
        # Continue green for another 5 seconds
        time.sleep(5)
        state = "YELLOW"
    
    elif state == "YELLOW":
        yellow_led.on()
        green_led.off()
        time.sleep(3)  # Yellow light stays on for 3 seconds
        state = "RED"

# Function to receive UART data from the other Pico
def check_uart():
    if uart.any():
        data = uart.read().decode('utf-8')  # Read UART data
        if data == "EW_RED":
            # Handle other Pico's red light event
            pass
        elif data == "EW_BUSY":
            # Handle too many cars on the other road
            other_road_cars += 1

# Main loop
while True:
    # Check UART for incoming data
    check_uart()
    
    # Run the traffic light state machine
    traffic_light_system()
    
    # Simulate sensor input for cars
    if not sensor_ns.value():
        other_road_cars += 1  # Increase car count for this road direction
    if not reset_button.value():
        state = "RED"  # Reset the system

