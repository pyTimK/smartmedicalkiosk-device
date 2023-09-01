import subprocess
from typing import Dict, Tuple
from random import randint
from time import sleep
import serial

pulse_calibration = 2


# if valid readings surpasses 6 counts, then average last 4 valid readings
_surpass_counts = 6
_get_average_count = 4 # Must be less than _surpass_counts

def _is_valid(pulse: int, spo2: int, has_hand: bool) -> bool:
    return has_hand and pulse > 60 and spo2 > 70

def has_hand() -> bool:
	ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=5)
	ser.reset_input_buffer()

	while True:
		if ser.in_waiting > 0:
			line = ser.readline().decode('utf-8').rstrip()
			values = line.split(" ")
			if len(values) != 3:
				# print("Unexpected reading from max30100: ")
				print(line)
				
				continue
				# raise Exception("Unexpected reading from max30100")
				
			if values[0] == 'End':
				continue

			pulse, spo2, has_hand = values
			print(values)
			pulse, spo2, has_hand = int(pulse), min(int(spo2), 100), bool(has_hand == '1')

			if has_hand:
				print("Has hand!")
				return True

def read_max30100() -> Tuple[int, int]:
	'''Returns pulse and spo2. Returns -1 on both of them on error'''
	try:
		ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=5)
		ser.reset_input_buffer()
		valid_readings = []

		while True:
			if ser.in_waiting > 0:
				line = ser.readline().decode('utf-8').rstrip()
				values = line.split("\t")
				if len(values) != 3:
					# print("Unexpected reading from max30100: ")
					print(line)
					continue
					# raise Exception("Unexpected reading from max30100")
					
				pulse, spo2, has_hand = values
				pulse, spo2, has_hand = int(pulse), min(int(spo2), 100), bool(has_hand)

				print(f"{pulse} {spo2} {has_hand}")
				
				if _is_valid(pulse, spo2, has_hand):
					valid_readings.append((pulse, spo2))
				
					if len(valid_readings) > _surpass_counts:
						valid_readings = valid_readings[-1*_get_average_count:]
						break
		
		pulse = sum(r[0] for r in valid_readings) // _get_average_count
		spo2 = sum(r[1] for r in valid_readings) // _get_average_count
		return pulse + pulse_calibration, spo2

	
	except Exception as e:
		print(e)
		return -1, -1

	#TODO for testing purposes only
	#return __random_temporary()



def __random_temporary() -> Tuple[int, int]:
	'''Mocks a max30100 in getting measures'''
	sleep(randint(4, 8))
	pulse = randint(50, 120)
	spo2 = randint(80, 100)
	return pulse, spo2


def _print_results(pulse: int, spo2: int):
	print(f"PULSE: {pulse}\tSPO2:{spo2}")


# TESTING ---------------------
# print(read_max30100())
# has_hand()
#------------------------------
