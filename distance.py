#!/usr/bin/python
# encoding:utf-8

import time  # Import time library
from time import sleep

import RPi.GPIO as GPIO  # Import GPIO library


def loop():
    GPIO.setmode(GPIO.BCM)  # Set GPIO pin numbering

    TRIG = 15  # Associate pin 15 to TRIG
    ECHO = 14  # Associate pin 14 to Echo
    distances = [0] * 10  # Creating a 10 rolling average
    count = 0  # creating a counter so that the pop function will only pop after the length of the distances is reached

    GPIO.setup(TRIG, GPIO.OUT)  # Set pin as GPIO out
    GPIO.setup(ECHO, GPIO.IN)  # Set pin as GPIO in

    while True:
        GPIO.output(TRIG, False)  # Set TRIG as LOW
        sleep(.5)  # Delay of 2 seconds

        def read():
            GPIO.output(TRIG, False)  # Set TRIG as LOW
            time.sleep(0.0005)  # Delay of 0.000005 seconds
            pulse_start = 0
            pulse_end = 0
            GPIO.output(TRIG, True)  # Set TRIG as HIGH
            time.sleep(0.00001)  # Delay of 0.00001 seconds
            GPIO.output(TRIG, False)  # Set TRIG as LOW

            while GPIO.input(ECHO) == 0:  # Check if Echo is LOW
                pulse_start = time.time()  # Time of the last  LOW pulse

            while GPIO.input(ECHO) == 1:  # Check whether Echo is HIGH
                pulse_end = time.time()  # Time of the last HIGH pulse

            pulse_duration = pulse_end - pulse_start  # pulse duration to a variable
            distance = pulse_duration * 17150  # Calculate distance
            distance = round(distance, 2) - 0.5  # Round to two decimal points
            return distance

        distance = read()

        if 20 < distance < 400:  # Is distance within range
            distances.append(distance)
            if count == len(distances):
                distances.pop(0)
            else:
                count = count + 1
        else:
            print(distances)
            print("Out of range " + str(distance))  # Distance with calibration

        average = round(sum(distances) / len(distances), 0)
        text = "Distance: " + str(average) + " cm."
        print(text)  # Distance with calibration


if __name__ == '__main__':
    loop()
