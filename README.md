# rPi_buttons

> Two buttons connected to raspberry pi to control hue lights.

I build a bedside table with integrated buttons to control my philips hue lights
#### Pictures (ToDo)

## Hardware 
* Push Button ([amazon](https://www.amazon.de/gp/product/B082B1F88S/ref=ppx_yo_dt_b_asin_title_o08_s00?ie=UTF8&psc=1)) 


## Wiring 
* Button 1: Pin 21
* Button 2: Pin 12

### Prerequisites
* huePyApi ([Github](https://github.com/Felix-Pi/huePyApi))

### Run script in background

run in background:
`nohup python3 /home/rPi_buttons/rPi_buttons.py > /dev/null &`

kill nohup
`ps ax | grep rPi_buttons.py --> kill PID`

run script on boot
`nano /etc/rc.local`

## Configuration
config.py
```
ip = ''
api_key = ''
```

## Functions
Button 1: 
  * short press: 
    * turn off every light
  * long press
    * set a scene
    
Button 2: 
  * short press: 
    * loop through scenes from hue dimmer switch (from bright to dark)
    * reverse senes at night (from dark to bright)
  * long press
    * set bright scene at day
    * set dark scene at night 

## Credits
* run script in background ([janakiev.com](https://janakiev.com/blog/python-background))
