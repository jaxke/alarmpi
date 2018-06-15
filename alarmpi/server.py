
from flask import Flask, jsonify, render_template, request
from pdb import set_trace as st
import json
import os


app = Flask(__name__)
alarms_file = "alarms.json"
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
class Config(object):
    pass#SERVER_NAME = "alarmpy"


@app.route('/')
def index():
    return render_template("main.html")


@app.route('/', methods=['POST'])
def ajax_post():
    post_data = json.loads(request.get_data().decode('utf-8'))
    #print("POST:" + post_data)
    if post_data.get('getAll'):
        return get_all()
    #if request.json.get('getAll'):
        #return get_all()
    if post_data.get('addAlarm'):
        return add_alarm(request.json)
    if post_data.get('removeAlarm'):
        return delete_alarm(request.json)
    if post_data.get('clearAll'):
        return clear_all()
    return ""


def get_all():
    if not os.path.isfile(alarms_file):
        open(alarms_file, 'a').close()
    json_data = ""
    with open(alarms_file, "r") as fr:
        json_data = fr.read()
    return json_data

def clear_all():
    open(alarms_file, 'w').close()
    return get_all()


# Use name as primary identifier
# Return True(on throwing KeyError) if an alarm with same identifier not in file.
def validate_id(id, alarms):
    try:
        if alarms[id]: return False
    except KeyError: return True


# Convert hours/minutes to a type with a leading zero if they satisfy conditions below.
# 1 => 01
def format_time(hr, min):
    if len(hr) == 1:
        hr = "0" + hr
    if len(min) == 1:
        min = "0" + min
    return hr, min

def all_days_to_numeric():
    return "0123456"

# Argument = JSON
def add_alarm(data_dict):
    alarm_name = data_dict['name']
    file_contents = get_all()
    d = { alarm_name: data_dict }
    try:
        del d[alarm_name]['name']
        del d[alarm_name]['addAlarm']   # Identifier for POST
        d[alarm_name]['hours'], d[alarm_name]['mins'] = format_time(d[alarm_name]['hours'], d[alarm_name]['mins'])
        if d[alarm_name]['days'] == "a":
            d[alarm_name]['days'] = all_days_to_numeric()
    except KeyError:
        print("KEY ERROR")
    if len(file_contents) > 0:
        file_contents = json.loads(get_all())
        if not validate_id(alarm_name, file_contents):
            return "NameException"
            # TODO JSON EXCEPTION

        # Merge data and old file contents
        file_contents = dict(file_contents, **d)
    else:
        file_contents = d
    write_to_file(file_contents)
    return "Success"

def delete_alarm(alarm_name):
    alarm_name = alarm_name['removeAlarm']
    file_contents = json.loads(get_all())
    # TODO Errors?
    if file_contents[alarm_name]:
        file_contents.pop(alarm_name)
    write_to_file(file_contents)
    return "Success"


# Argument = dict
def write_to_file(data):
    with open(alarms_file, "w") as fw:
        json.dump(data, fw)
