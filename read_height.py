from gpiozero import Button, DistanceSensor
from signal import pause
import time
import warnings

measure_button = Button(25)
height_offset = 100
time_delay_sec = 3

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    distance_sensor = DistanceSensor(echo=21, trigger=20)

def read_height():
    print("Waiting for button to be pressed...")
    measure_button.wait_for_press()
    print("Getting height...")

    start_time = time.time()
    while time.time() - start_time < time_delay_sec:
        height = int(distance_sensor.value * 100)
        print(f"height: {height}")
        
    print(f"Done. Height: {height}")
    return height



