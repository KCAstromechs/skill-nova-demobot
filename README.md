# skill-nova-demobot
Mycroft Skill for running the Nova outreach / demo robot
```
             ------------------------------------------------------------------------------------------------
RCA Port    | 2  | 4 | 6 | 8 | 10 | 12 | 14 | 16 | 18 | 20 | 22 | 24 | 26 | 28 | 30 | 32 | WH | 36 | GN | 40 |
            | BK | 3 | 5 | 7 |  9 | 11 | 13 | 15 | 17 | 19 | 21 | 23 | 25 | 27 | 29 | RD | 33 | 35 | 37 | 39 |
             ------------------------------------------------------------------------------------------------
             
 HDMI                         Ethernet                        USB     USB
```

BK = Black = Ground (pin 1)
GN = Green = GPIO_26 (pin 38) = Signal1
RD = Red = GPIO_8 (pin 31) = Clock
WH = White = GPIO_11 (ping 34) = Signal2

see the Mark 1 pin mapping: https://github.com/MycroftAI/enclosure-mark1#io-pins

# Physical connection

* Attach the 3-pin header to the 3-pin connector on the coiling cable, connecting colors to the same-colored wire except the blue, which goes to black.
* Insert the blue jumper wire into first header pin at the back of Mycroft.  Similary, put the red in the 31st hole and put the yellow in the 38th hole.  (See the block header illustration above)
* Connect the power lead with the barrel connector to the back of Mycroft
* Connect the three standard batteries
* Attach the "Mycroft" phone
