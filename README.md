# Alarmpy
Alarm clock written in Python mainly targeted to Linux and later Raspberry Pi with harware controls
## Requiremens
* Flask
* ffmpeg(ffplay)
## Components
* Web frontend written in Javascript using jQuery for AJAX calls and DOM manipulation
* Bulma CSS
* Web backend written in Python using Flask
* Alarm clock written in Python
### Frontend
* 100% AJAX
* Lists set alarms  
![frontend](https://raw.githubusercontent.com/jaxke/alarmpy/master/Screenshot%20from%202018-05-15%2012-57-10.png)
### Backend
* Return and change alarm info from/to local JSON file that keeps the alarms
Flask setup:  
```export FLASK_APP=server.py```  
```flask run```

### Alarm clock
* Terminal frontend
* Uses ffplay for alarm sound file playback
## TODO
- [ ] Full Raspberry and Orange Pi support(hardware and software info will be updated here)
