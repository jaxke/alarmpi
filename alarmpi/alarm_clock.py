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
import RPi.GPIO as GPIO


# TODO assumes port 5000
if len(argv) == 2:
    serv_ip = "http://" + argv[1] + ":5000"
elif len(argv) == 1:
    print("Using localhost server(no arguments passed)") # TODO this print is overwritten immediately
    serv_ip = "http://127.0.0.1:5000"
else:
    print("You can only pass one argument!")
    exit(1)

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
    print(name)
    exc = ["ffplay", "-nodisp", "-autoexit", sound_file]
    FNULL = open(os.devnull, 'w')
    proc = subprocess.Popen(exc, stdout=FNULL, stderr=subprocess.STDOUT)
    #kill = str(input("Enter 'a': "))
    #input("input")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(2,GPIO.IN)
    while True:
    	if not GPIO.input(2):
            proc.kill()
            break
    #if kill == 'a':


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

def days_to_list(days):
    return [x for x in days]

def clear_term_window():
    os.system('clear')

def print_current_time(h, m, s):
    print("CURRENT TIME: {}:{}:{}".format(timeH, timeM, timeS))


def request_alarms():
    r = requests.post(serv_ip, data=json.dumps({'getAll': 1}))
    if r.status_code == 200:
        if r.text:
            return json.loads(r.text)
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
            print("Connection error, trying to re-establish link...")
            for i in [0, 1, 2]:
                sleep(5)
                alarms_json = request_alarms()
                if alarms_json != "connection error":
                    break
                if i == 2:
                    print("ERROR: Cannot re-establish connection!")
        alarms = []
        # If key values were found in file
        if alarms_json:
            for alarm_name in alarms_json.keys():
                if alarm_name in alarms_done:
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
        time.sleep(1)
