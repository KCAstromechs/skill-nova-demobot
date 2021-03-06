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
from time import sleep

from threading import Thread, Lock


import RPi.GPIO as GPIO
import time
clockPin = 8
signalPin = 26
incomingSignalPin = 11   # not tested yet
isDemo = True            # Controls whether "Hey Mycroft" fires the ball -- default Yes


is_master = False        # True when Mycroft sends signals to the robot
                         # False when the robot sends singals to Mycroft

class astrogpio(MycroftSkill):
    colorToggle = False

    def __init__(self):
        super(astrogpio, self).__init__(name="astrogpio")

        if is_master:
            # This skill will drive the communication and clock
            # initilization code for the GPIO board.
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(signalPin, GPIO.OUT)
            GPIO.setup(clockPin, GPIO.OUT)
            GPIO.output(signalPin, False)
            GPIO.output(clockPin, False)
            self.threadComms = None
        else:
            # Java will drive the communication, listen on a thread
            self.threadComms = RobotCommThread(self)

    def initialize(self):
        self.log.debug("Loaded!")
        self.add_event('mycroft.mark1.demo', self.demo)

    def shutdown(self):
        if self.threadComms.is_alive():
            self.threadComms.shutdown()

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
        global isDemo
        if isDemo:
            isDemo = False
            if is_master == True:
                self.remove_event('recognizer_loop:record_begin', self.handle_shoot_ball)
                self.speak("Entering demo mode, say 'Hey Mycroft' to launch a ball")
            self.speakRandomAffirmation()
        else:
            isDemo = True
            if is_master == True:
                self.add_event('recognizer_loop:record_begin', self.handle_shoot_ball)
                self.speak("Exited demo mode")
            self.speakRandomNegation()

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

    # BELOW are actions that are triggered by Java
    def execute_command(self, commandID):
        if commandID == 1:
            # self.speakRandomAffirmation()
            self.speakRollItBackToMe()
        if commandID == 2:
            self.wink()
        if commandID == 3:
            self.speakHereItComes()
        if commandID == 4:
            self.speakRandomGreeting()
        if commandID == 5:
            self.speakRandomGoodbye()
        if commandID == 6:
            self.speakWouldYouLikeToPlay()
        if commandID == 7:
            self.speakRandomNegation()

    def wink(self):
        self.enclosure.eyes_blink(choice(["r", "l"]))

    def speakRandomGreeting(self):
        self.speak_dialog("greeting")

    def speakRandomGoodbye(self):
        self.speak_dialog("goodbye")

    def speakRollItBackToMe(self):
        self.speak_dialog("rollItBackToMe")

    def speakRandomNegation(self):
        self.speak_dialog("negativeResponse")
        self.log.debug("NEGATION")

    def speakRandomAffirmation(self):
        self.speak_dialog("affirmativeResponse")
        self.log.debug("AFFIRMATION")

    def speakWouldYouLikeToPlay(self):
        self.speak_dialog("wouldYouLikeToPlay")

    def speakHereItComes(self):
        self.speak_dialog("hereItComes")


#####################################################################
# Serial Communication management

class RobotCommThread(Thread):

    def __init__(self, skill):
        super(RobotCommThread, self).__init__()
        self.parent_skill = skill
        self.should_run = True

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(signalPin, GPIO.IN)
        GPIO.setup(clockPin, GPIO.IN)
        self.start()

    def shutdown(self):
        self.should_run = False
        self.join() # Wait until the run() finishes before returning

    def run(self):
        commandID = None
        commandReady = False
        last_clock = GPIO.input(clockPin)
        self.parent_skill.log.info("Starting pin listener thread")

        while self.should_run:
            clock = GPIO.input(clockPin)
            if clock == 1:
                self.parent_skill.log.info("Start receiving command")
                last_clock = 1
                commandID = 0
                # Clock changed!
                for i in range(3):
                    while clock == last_clock:
                        clock = GPIO.input(clockPin)
                        sleep(.01)
                    self.parent_skill.log.info("bit " + str(i + 1) + "read")
                    if GPIO.input(signalPin):
                        commandID += 1 << (2-i)
                    last_clock = clock
                self.parent_skill.execute_command(commandID)
                self.parent_skill.log.info("Received command ID " + str(commandID))
                sleep(.1)

        # self.parent_skill.log.info("Stopping pin listener thread")


def create_skill():
    return astrogpio()
