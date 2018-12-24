# Copyright 2017, Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os.path import dirname, join
from mycroft import MycroftSkill, intent_handler, intent_file_handler
from mycroft.util.parse import extract_number


from adapt.intent import IntentBuilder
from mycroft.audio import is_speaking
from mycroft.skills.core import MycroftSkill, intent_handler
from random import choice

import RPi.GPIO as GPIO
import time
clockPin = 8
signalPin = 26
incomingSignalPin = 27   # not tested yet


class astrogpio(MycroftSkill):
    colorToggle = False

    def __init__(self):
        super(astrogpio, self).__init__(name="astrogpio")
        GPIO.setmode(GPIO.BCM)
        #GPIO.setup(signalPin, GPIO.IN)
        GPIO.setup(signalPin, GPIO.OUT)
        GPIO.setup(clockPin, GPIO.OUT)
        GPIO.output(signalPin, False)
        GPIO.output(clockPin, False)
        self.latch = False
        self.collector = True

    def initialize(self):
        # TODO
        #self.schedule_repeating_event(self.handle_callback, 0, 1)
        self.log.debug("Loaded!")

    def handle_callback(self, message):
        state = GPIO.input(incomingSignalPin)
        self.log.info("Running callback:"+ str(state))
        if not self.latch and state == 1 and not is_speaking():
            self.speak("you got no jams")
            if astrogpio.colorToggle:
                self.enclosure.eyes_color(255,0,0)
                astrogpio.colorToggle = False
            else:
                self.enclosure.eyes_color(0,255,0)
                astrogpio.colorToggle = True

                self.latch = True
        else:
            self.latch = False

    @intent_file_handler('collector.intent')
    def handle_toggle_collector(self, message):
        self.speak("Received toggle")
        self.generate_msg([0,0,1,0])

    @intent_file_handler('shooter.intent')
    def handle_shoot_ball(self, message):
        self.speak("firing ball")
        self.generate_msg_experiment([1,1,0,0,1,0,0,0,0,0])

    @intent_file_handler('driveStraight.intent')
    def handle_drive_straight(self, message):
        self.speak("Driving straight")
        # self.log.info("Utterance: "+)
        utt = message.data["utterance"]
        dist = extract_number(str(utt))
        binarMessage = '{0:06b}'.format(int(dist))
        self.log.info("Binary = " + binarMessage)
        binarMessage = binarMessage[::-1]
        self.log.info("Dist = "+str(dist))
        self.log.info("Reverse binary = " + binarMessage)
        self.generate_msg_from_string('eleven', str(utt))
        #self.generate_msg_experiment([1,1,0,0,1,0,0,0,1,0])
    def generate_msg_from_string(self, command, msg):
        data = exxtract_number(msg)
        data = '{0:06b}'.format(int(data))
        data = data[::-1]
        command = extract_number(command)
        command = '{0:04b}'.format(int(command))
        command = command[::-1]
        self.log.info("data = " + data)
        self.log.info("command = " + command)
        self.log.info("SSS " + str(msg))
        clockState = True
        GPIO.output(clockPin, clockState)
        #self.log.info("clock=" + str(bool(clockState)))
        time.sleep(.25)
        for i in command:
            GPIO.output(signalPin, bool(int(i)))
            #time.sleep(.1)
            clockState = not clockState
            GPIO.output(clockPin, clockState)
            #self.log.info("clock=" + str(bool(clockState)))
            self.log.info("SSS " + str(bool(int(i))))
            time.sleep(.1)
        for i in data:
            GPIO.output(signalPin, bool(int(i)))
            #time.sleep(.1)
            clockState = not clockState
            GPIO.output(clockPin, clockState)
            #self.log.info("clock=" + str(bool(clockState)))
            self.log.info("SSS " + str(bool(int(i))))
            time.sleep(.1)
        GPIO.output(signalPin, False)
        GPIO.output(clockPin, False)
        self.log.info("clock=" + str(bool(False)))
        time.sleep(2.5)
    def generate_msg(self, msg):
        self.log.info("SSS " + str(msg))
        GPIO.output(signalPin, True)
        time.sleep(.25)
        for i in msg:
            GPIO.output(signalPin, bool(i))
            self.log.info("SSS " + str(bool(i)))
            time.sleep(.25)
        GPIO.output(signalPin, False)
        time.sleep(100)

    def generate_msg_experiment(self, msg):
        self.log.info("SSS " + str(msg))
        clockState = True
        GPIO.output(clockPin, clockState)
        self.log.info("clock=" + str(bool(clockState)))
        time.sleep(.25)
        for i in msg:
            GPIO.output(signalPin, bool(i))
            #time.sleep(.1)
            clockState = not clockState
            GPIO.output(clockPin, clockState)
            self.log.info("clock=" + str(bool(clockState)))
            self.log.info("SSS " + str(bool(i)))
            time.sleep(.1)
        GPIO.output(signalPin, False)
        GPIO.output(clockPin, False)
        self.log.info("clock=" + str(bool(False)))
        time.sleep(2.5)
def create_skill():
    return astrogpio()

