import subprocess

# Dependency: cec-utils

# TV Status: "echo pow 0 | cec-client -s -d 1"
# Turn off: "echo standby 0 | cec-client -s -d 1"
# Turn on: "echo on 0 | cec-client -s -d 1"

status = ("echo", "pow", "0")
turn_on = ("echo", "on", "0")
turn_off = ("echo", "standby", "0")
pipe = ("cec-client", "-s", "-d", "1")


def check_tv_status():
    p = subprocess.Popen(status, stdout=subprocess.PIPE)
    out = subprocess.check_output(pipe, stdin=p.stdout)
    p.wait()
    out = out.decode('utf-8').split("power status: ")[1].strip()

    if out in ["on", "standby"]:
        return out
    else:
        return False


def tv_on():
    p = subprocess.Popen(turn_on, stdout=subprocess.PIPE)
    subprocess.check_output(pipe, stdin=p.stdout)
    p.wait()


def tv_off():
    p = subprocess.Popen(turn_off, stdout=subprocess.PIPE)
    subprocess.check_output(pipe, stdin=p.stdout)
    p.wait()
