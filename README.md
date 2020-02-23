# skill-nova-demobot
Mycroft Skill for running the Nova outreach / demo robot

# Physical connection

* Attach the 4-wires from the coiling cable into the I/O Pins at the back of Mycroft.  See below.
* Connect the power lead with the barrel connector to the power jack in the back of back of Mycroft
* Connect the three (3) standard batteries
  - One to power Mycroft
  - One to power the robot
  - One to power lights
* Attach the "Mycroft" phone

# Control cheat sheet

### Wink
  (**Joystick button ??**)
  
  Just to be cute
  
  
### "Here it comes!"
  (**Joystick button ??**)

  Warn a child that the robot is about to launch a ball for them to catch
  
  
### "Hello!"
  (**Joystick button ??**)

  Greet a human
  
  
### "Goodbye!"
  (**Joystick button ??**)

  Politely say goodbye to the human
  
  
### "Would you like to play catch?"
  (**Joystick button ??**)

  Ask the human if they want to interact
  
  
### "No"
  (**Joystick button ??**)

  Simple generic answer for random questions



# Mycroft I/O Pins

```
             ------------------------------------------------------------------------------------------------
RCA Port    | 2  | 4 | 6 | 8 | 10 | 12 | 14 | 16 | 18 | 20 | 22 | 24 | 26 | 28 | 30 | 32 | WH | 36 | GN | 40 |
            | BK | 3 | 5 | 7 |  9 | 11 | 13 | 15 | 17 | 19 | 21 | 23 | 25 | 27 | 29 | RD | 33 | 35 | 37 | 39 |
             ------------------------------------------------------------------------------------------------
             
 HDMI                         Ethernet                        USB     USB
```


![#000000](https://placehold.it/15/000000/000000?text=+) = Black = Ground (pin 1)<br/>
![#3cf015](https://placehold.it/15/3cf015/000000?text=+) = Green = GPIO_26 (pin 38) = Signal1<br/>
![#f03c15](https://placehold.it/15/f03c15/000000?text=+) = Red = GPIO_8 (pin 31) = Clock<br/>
![#dddddd](https://placehold.it/15/ffeeff/000000?text=+) = White = GPIO_11 (ping 34) = Signal2<br/>

see the Mark 1 pin mapping: https://github.com/MycroftAI/enclosure-mark1#io-pins

