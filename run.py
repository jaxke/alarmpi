#!/usr/bin/env python

import subprocess
import os
import time

SOURCE_DIR = os.getcwd()


def main():
    FNULL = open(os.devnull, 'w')
    subprocess.Popen(("export FLASK_APP=" + SOURCE_DIR + "/alarmpi/server.py").split(" "), shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
    flask_run = subprocess.Popen(["flask", "run", "--host=0.0.0.0"], stdout=FNULL, stderr=subprocess.STDOUT)
    time.sleep(5)
    alarm_clock = subprocess.Popen(["python", SOURCE_DIR + "/alarmpi/alarm_clock.py"])

main()
