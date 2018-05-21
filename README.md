# Alarmpy
Alarm clock written in Python mainly targeted to Raspberry Pi
## Requiremens
* Flask
* ffmpeg(ffplay)
* RPi.GPIO
## Components
* Web frontend written in Javascript using jQuery for AJAX calls and DOM manipulation
* Bulma CSS
* Web backend written in Python using Flask
* Alarm clock written in Python
### Frontend
* 100% AJAX
* Lists set alarms  
![frontend](https://github.com/jaxke/alarmpi/blob/master/Screenshot%20from%202018-05-15%2012-57-10.png)

### Backend
* Return and change alarm info from/to local JSON file that keeps the alarms  

Setup:  
* Clone the repo into your Pi and run alarm_clock.py as root(GPIO requires it).  
* Access the web server at ```http://[IP ADDR OF PI]:5000```  
Flask setup:  
```export FLASK_APP=server.py```  
```flask run --host="0.0.0.0"```  

### Alarm clock
* Terminal frontend
* Uses ffplay for alarm sound file playback

## Pi
In series: GPIO port 2 -> 10k ohm resistor -> button switch -> earth  
Press button for ~1 second and the alarm will dismiss

## TODO
- [x] Raspberry Pi GPIO  
- [ ] Clean up terminal interface  
- [ ] Auto IP address(must be configured in source ATM)  
- [ ] LED Ambient light
