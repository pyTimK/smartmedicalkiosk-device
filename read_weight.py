import time
import sys
from hx711 import HX711
from typing import List

_referenceUnit = 23.76
_adjust_add = 0.3
_min_weight_kg = 20.0

### INITIALIZE
hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
# HOW TO CALCULATE THE REFFERENCE UNIT
# 184000 / 2000 = 92.
hx.set_reference_unit(_referenceUnit)
hx.reset()
hx.tare()
# print("Tare done! Add weight now...")

def __get_weight():
    return max(hx.get_weight(5) / 1000, 0.0)


def deviation_within_x(readings: List[float], x: float)-> bool: 
    average = sum(readings) / len(readings)
    for reading in readings:
        if abs(reading - average) > x:
            return False
    
    return True


### init
def read_weight_init():
    val = __get_weight()

    while val < _min_weight_kg:
        print(f"Weight: {val:.2f}")

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)
        val = __get_weight()

    return val + _adjust_add


### read
def read_weight():
    readings = [0.0, 0.0, 0.0, 0.0, 0.0]

    while True:
        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

        val = __get_weight()
        print(f"Weight: {val:.2f}")

        if val < _min_weight_kg:
            continue

        readings.pop()
        readings.insert(0, val)

        if deviation_within_x(readings, 2.0):
            average = sum(readings) / len(readings)
            return average + _adjust_add




# read_weight_init()
# print(f"Final Weight: {read_weight()}")


