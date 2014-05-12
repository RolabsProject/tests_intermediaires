#!/usr/bin/python
# indent-mode: spaces, indentsize: 4, encoding: utf-8
# © 2011 con-f-use@gmx.net.
# Use permitted under MIT license:
# http://www.opensource.org/licenses/mit-license.php (NO WARRANTY IMPLIED)
"""A Wiimote script to control totem and amarok under Ubuntu.

Provides a rudimentary interface to:
-Check battery status of the Wiimote.
-Switch an led on the Wiimote.
-Start Amarok.
-Pause/contiue playing.
-Skip to next/last track.
-Control the system volume over pulseaudio

Needs the package 'python-cwiid', 'amarok' and or 'totem' to be installed.

Globals:

wiimote -- the wiimote object
led -- the status of the led (on/off)

"""

import cwiid
import sys
import os

def main():
    """PC-side interface handles interaction between pc and user.

    b -- battery status
    l -- toggle led
    q -- quit
    h -- print help
    """
    global wiimote
    connect_wiimote()

    #Print help text ont startup
    print 'Confirm each command with ENTER.'
    hlpmsg =    'Press q to quit\n'\
                'b for battery status\n'\
                'l to toggle the led on/off\n'\
                'h or any other key to display this message.'
    print hlpmsg

    #Main loop for user interaction
    doLoop = True
    while doLoop:
        c = sys.stdin.read(1)
        if c == 'b':    # battery status
            state = wiimote.state
            bat = int(100.0 * state['battery'] / cwiid.BATTERY_MAX)
            print bat
        elif c == 'l':  # toggle led
            toggle_led()
        elif c == 'q':  # exit program
            doLoop = False
        elif c == '\n': # ignore newlines
            pass
        else:           # print help message when no valid command is issued
            print hlpmsg

    #Close connection and exit
    wiimote.close()

def connect_wiimote():
	"""Connets your computer to a Wiimote."""
	print 'Put Wiimote in discoverable mode now (press 1+2)...'
	global wiimote
	while True:
		try:
			wiimote = cwiid.Wiimote('00:1F:C5:47:E4:F1')#add address of Wiimote here for speedup)
			break
		except:
			continue
	wiimote.mesg_callback = callback
	#Set Wiimote options
	global led
	led = True
	wiimote.led = cwiid.LED1_ON
	wiimote.rpt_mode = cwiid.RPT_BTN
	wiimote.enable(cwiid.FLAG_MESG_IFC)

def callback(mesg_list, time):
    """Handels the interaction between Wiimote and user.

    A and B together    -- toggle led
    A                   -- play/pause
    up / down           -- fast forward / backward
    right / left        -- next / previous trakc
    + / -               -- increase / decreas volume

    """
    for mesg in mesg_list:
        # Handle Buttonpresses - add hex-values for simultaneous presses
        # Buttons not listed: 0x4 - B, 0x1 - 2, 0x2 - 1 | just babytown frolics
        if mesg[0] == cwiid.MESG_BTN:
            if   mesg[1] == 0x8:    # A botton
		print "A"
            elif mesg[1] == 0x4:    # B together
		print "B"
            elif mesg[1] == 0x800:  # Up botton
		print "UP"
            elif mesg[1] == 0x100:  # Left botton
		print "LEFT"
            elif mesg[1] == 0x200:  # Right botton
		print "RIGHT"
            elif mesg[1] == 0x400:  # Down botton
		print "DOWN"
            elif mesg[1] == 0x10:   # Minus botton
		print "-"
            elif mesg[1] == 0x1000: # Plus botton
		print "+"
            elif mesg[1] == 0x80:   # home botton
		print "HOME"
        # Handle errormessages
        elif mesg[0] == cwiid.MESG_ERROR:
            global wiimote
            wiimote.close()
            connect_wiimote()

def toggle_led():
    """Toggles first led on Wiimote on/off."""
    global led
    if led == True:
        led = False
        wiimote.led = 0
    else:
        led = True
        wiimote.led = cwiid.LED1_ON


main()
