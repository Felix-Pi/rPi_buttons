import RPi.GPIO as GPIO

import time

from config import ip, api_key
from huePyApi import Hue


debounce_time = 0.22
long_press_time = 0.8

index = 0

hue = Hue.Hue(ip=ip, api_key=api_key)
group_0 = hue.get_group(0)
group_5 = hue.get_group(5)
scenes_dimmer = hue.get_resourcelink(1063).getLinkedScenes()
scenes_dimmer.reverse()
scenes_dimmer.append('8CwvoHEQe02ATlp')  # (schlafen II)

class Button:
    id_counter = 0

    def __init__(self, title, gpioPin, btnAction):
        self.id = Button.id_counter
        self.title = title
        self.gpioPin = gpioPin
        self.btnAction = btnAction

        Button.id_counter += 1

    def onButtonPressed(self, channel):
        timer_start = time.time()

        while GPIO.input(self.gpioPin) == GPIO.LOW:
            time.sleep(0.01)

        timer_duration = time.time() - timer_start

        # debounce
        if timer_duration > debounce_time:

            long_press = False

            if timer_duration > long_press_time:
                long_press = True

            print('button press detected: id={}, long_press={}, duration={}\n'.format(self.id, long_press,
                                                                                      timer_duration))

            self.btnAction(long_press)


def getTimes():
    t0 = time.time()
    t0_string = time.strftime('%H:%M', time.localtime(t0))

    t1 = t0 - 1 * 60
    t1_string = time.strftime("%H:%M", time.localtime(t1))

    return t0_string, t1_string


def btn_1_action(long_press):
    if not long_press:
        group_0.set_on(False)

    if long_press:
        group_5.set_scene(hue.get_scene('7gzrbM3Nh83Qjr0'))  # (chillen II)


def btn_2_action(long_press):
    if not long_press:
        global index
        print('index', index)
        curr_time, time_minus_one = getTimes()

        if not '06.00' <= curr_time <= '21.30':
            scenes_dimmer.reverse()

        if time_minus_one > curr_time:
            index = 0
        else:
            index += 1
            if index >= len(scenes_dimmer):
                index = 0

        group_5.set_scene_by_id(scenes_dimmer[index])

    if long_press:
        curr_time = getTimes()[0]

        if '06.00' <= curr_time <= '21.30':
            scene = 'mksQRqnXOPeutFA'  # (konzentrieren)
        else:
            scene = '8CwvoHEQe02ATlp'  # (schlafen II)
        group_5.set_scene_by_id(scene)


if __name__ == '__main__':
    buttons = [
        Button('Bett 01', 21, btn_1_action),
        Button('Bett 02', 12, btn_2_action),
        # Button('Fensterbank 16', 16)
    ]

    GPIO.setmode(GPIO.BCM)

    for btn in buttons:
        GPIO.setup(btn.gpioPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(btn.gpioPin, GPIO.RISING, callback=btn.onButtonPressed, bouncetime=1200)
        print('initialized Button \'{}\': id={}, pin={}'.format(btn.title, btn.id, btn.gpioPin))

    print('waiting for input')
    while True:
        time.sleep(0.01)
