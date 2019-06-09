# Copyright 2018, Astromechs FTC (#3409)
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
isDemo = True            # Controls whether "Hey Mycroft" fires the ball -- default Yes

class astrogpio(MycroftSkill):
    colorToggle = False

    def __init__(self):
        super(astrogpio, self).__init__(name="astrogpio")
        #initilization code for the GPIO board.
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(signalPin, GPIO.OUT)
        GPIO.setup(clockPin, GPIO.OUT)
        GPIO.output(signalPin, False)
        GPIO.output(clockPin, False)

    def initialize(self):
        self.log.debug("Loaded!")
        self.add_event('mycroft.mark1.demo' self.demo)

    #Sends GPIO command to trigger collector toggle
    @intent_file_handler('collector.intent')
    def handle_toggle_collector(self, message):
        self.speak("Received toggle")
        utt = str(message.data.get("utterance", ""))
        self.send_msg_GPIO(4, utt)

    #Sends GPIO command to trigger a ball shot
    @intent_file_handler('shooter.intent')
    def handle_shoot_ball(self, message):
        self.log.info("Firing ball")
        self.speak("firing ball")
        utt = str(message.data.get("utterance", ""))
        self.send_msg_GPIO(3, utt)

    def demo(self):
        if isDemo:
            isDemo = False
            self.remove_event('recognizer_loop:record_begin', self.handle_shoot_ball)
            self.speak("Entering demo mode, say 'Hey Mycroft' to launch a ball")
        else:
            isDemo = True
            self.add_event('recognizer_loop:record_begin', self.handle_shoot_ball)
            self.speak("Exited demo mode")

    #Sends GPIO command to trigger a straight drive with an distance of 0-63 inches
    @intent_file_handler('driveStraight.intent')
    def handle_drive_forwards(self, message):
        self.speak("Driving straight")
        utt = str(message.data["utterance"])
        self.send_msg_GPIO(11, utt)

    #Sends GPIO command to trigger a straight backwards drive with an distance of 0-63 inches
    @intent_file_handler('driveBackwards.intent')
    def handle_drive_backwards(self, message):
        self.speak("Driving backwards")
        utt = str(message.data["utterance"])
        self.send_msg_GPIO(14, utt)


    def send_msg_GPIO(self, command, msg):
        #extracts number from utterance
        data = extract_number(msg)

        #converts number to binary with at least 6 digits including leading zeros
        data = '{0:06b}'.format(int(data))

        #reverses the order of the binary to allow the OpMode to read the information as it reads it
        data = data[::-1]

        #repeats the last two steps
        command = '{0:04b}'.format(int(command))
        command = command[::-1]

        self.log.info("data = " + data)
        self.log.info("command = " + command)
        self.log.info("SSS " + str(msg))

        #turns on the clockpin for .1s to signify a message is about to be sent
        clockState = True
        GPIO.output(clockPin, clockState)
        time.sleep(.1)

        for i in command:
            # send the next bit in the 4-bit command
            GPIO.output(signalPin, bool(int(i))) #writes the bit onto the single wire
            clockState = not clockState #flips the clockpin tracker
            GPIO.output(clockPin, clockState) #changes state of clockpin to match the tracker
            self.log.info("SSS " + str(bool(int(i))))

            #wait a lil bit for the OpMode to catch up
            time.sleep(.1)

        for i in data:
            # send the next bit in the 6-bit data
            GPIO.output(signalPin, bool(int(i))) #writes the bit onto the single wire
            clockState = not clockState #flips the clockpin tracker
            GPIO.output(clockPin, clockState) #changes state of clockpin to match the tracker
            self.log.info("SSS " + str(bool(int(i))))

            #wait a lil bit for the OpMode to catch up
            time.sleep(.1)

        #resets both GPIO pins
        GPIO.output(signalPin, False)
        GPIO.output(clockPin, False)
        self.log.info("clock=" + str(bool(False)))
        time.sleep(2.5)


    # BELOW is actions that are triggered by Java

    def execute_command(self, commandID):
        if commandID = 1:
            wink()
        if commandID = 2:
            speakRandomGreeting()
        if commandID = 3:
            speakRandomGoodbye()
        if commandID = 4:
            speakRandomAffirmation()
        if commandID = 5
            speakRandomNegation()


    def wink():
        self.enclosure.eyes_blink(choice(["r", "l"]))
    def speakRandomGreeting():
        self.speak_dialog("greeting")
    def speakRandomGoodbye():
        self.speak_dialog("goodbye")
    def speakRandomNegation():
        self.speak_dialog("negativeResponse")
    def speakRandomAffirmation():
        self.speak_dialog("affirmativeResponse")

def create_skill():
    return astrogpio()

