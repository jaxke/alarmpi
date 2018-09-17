import subprocess
import datetime
import time
from time import gmtime, strftime
from pdb import set_trace as st
import json
import os
import requests
from sys import argv, exit
from time import sleep
import sys
try:
    import RPi.GPIO as GPIO
    nogpio = False
except ImportError:
    nogpio = True
    print("gpio module not found")

serv_ip = None

if len(argv) in [2,3]:
    if len(argv) == 3:
        serv_ip = "http://" + argv[2] + ":5000"
    gpio_in_pin = argv[1]
    try:
        gpio_in_pin = int(gpio_in_pin)
        print("Using GPIO pin number " + str(gpio_in_pin))
    except ValueError:
        print("First argument must be the GPIO pin number!")
        exit(1)
elif len(argv) == 1:
    nogpio = True
    print("GPIO pin not specified in args(nogpio mode)!")
    sleep(3)    # To display the print above
else:
    print("Too many arguments!")
    exit(1)

if not serv_ip:
    serv_ip = "http://127.0.0.1:5000"
    print("IP not specified, using localhost.")





WORKING_DIR = os.getcwd()
sound_file = WORKING_DIR + "/alarm.mp3"


def get_current_time():
    wkday = datetime.datetime.today().weekday()
    timeH = time.strftime("%H", time.localtime())
    timeM = time.strftime("%M", time.localtime())
    timeS = time.strftime("%S", time.localtime())
    return [str(wkday), timeH, timeM, timeS]


def ring_alarm(name):
    clear_term_window()
    print("Alarm " + name)
    exc = ["ffplay", "-nodisp", "-autoexit", sound_file]
    # Suppress shell output
    FNULL = open(os.devnull, 'w')
    proc = subprocess.Popen(exc, stdout=FNULL, stderr=subprocess.STDOUT)
    if not nogpio:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(gpio_in_pin, GPIO.IN)
        # Press GPIO2 to dismiss(the idea is to use a switch)
        while True:
            if not GPIO.input(gpio_in_pin):
                proc.kill()
                break
    # Use input to dismiss if GPIO wasn't imported
    else:
        while True:
            # TODO
            i = str(input("> "))
            if i == "a":
                proc.kill()


class Alarm:
    name = ""
    hour = ""
    mins = ""

    def __init__(self, name, hours, mins):
        self.name = name
        self.hours = hours
        self.mins = mins


# Lists alarms that have rang today, clear after a day has passed.
alarms_done = []


# 123 => [1, 2, 3]
def days_to_list(days):
    return [x for x in days]


def clear_term_window():
    os.system('clear')


def print_current_time(h, m, s):
    print("CURRENT TIME: {}:{}:{}".format(timeH, timeM, timeS))


# $ flask run
def request_alarms():
    r = requests.post(serv_ip, data=json.dumps({'getAll': 1}))
    if r.status_code == 200:
        if r.text:
            return json.loads(r.text)
        # No alarms, return None
        else:
            return
    else:
        return "connection error"


def list_alarms_tomorrow(alarms, wkday_now):
    alarms_tomorrow = []
    for alarm in alarms:
        for wkday_alarm in days_to_list(alarms[alarm]['days']):
            if int(wkday_now) + 1 == int(wkday_alarm):
                alarms_tomorrow.append(alarm)
    if len(alarms_tomorrow) > 0:
        print("\nALARMS TOMORROW:\n")
        for al in alarms_tomorrow:
            print("{}\t\t{}:{}".format(al, alarms[al]['hours'], alarms[al]['mins']))


# Attempt to reconnect to server 3 times
def attempt_to_reconnect():
    print("Connection error, trying to re-establish link...")
    for i in [0, 1, 2]:
        sleep(5)
        alarms_json = request_alarms()
        if alarms_json != "connection error":
            # This can still be None, but getting the response is the idea
            return alarms_json
        if i == 2:
            print("ERROR: Cannot re-establish connection!")
            exit(1)


if __name__ == "__main__":
    while True:
        clear_term_window()
        now = get_current_time()
        wkday, timeH, timeM, timeS = now
        # Clear this array at the start of a day
        if timeH == "00" and timeM == "00":
            alarms_done = []
        alarms_json = request_alarms()
        if alarms_json == "connection error":
            # The function will terminate program if fails or return json
            alarms_json = attempt_to_reconnect()
        alarms = []
        # If key values were found in file(retval is not None)
        if alarms_json:
            for alarm_name in alarms_json.keys():
                if alarm_name in alarms_done:   # Skip alarms that have rang today
                    continue
                al = alarms_json[alarm_name]
                # Also disregard alarms that have passed once the program is ran
                if al['hours'] <= timeH and al['mins'] < timeM:
                    continue
                if wkday in days_to_list(al['days']):
                    alarm_instance = Alarm(alarm_name, al['hours'], al['mins'])
                    alarms.append(alarm_instance)
        print_current_time(timeH, timeM, timeS)
        if len(alarms)  == 0:
            print("No alarms set for today!")
        for al in alarms:
            print("{}\t\t{}:{}".format(al.name, al.hours, al.mins))
        if alarms_json:
            list_alarms_tomorrow(alarms_json, wkday)
        for al in alarms:
            if timeH == al.hours and timeM == al.mins:
                ring_alarm(al.name)
                alarms_done.append(al.name)
        # Set time resolution to 1 sec so that time print updates every second
        time.sleep(1)
