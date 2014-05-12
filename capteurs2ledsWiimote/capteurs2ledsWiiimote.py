#!/usr/bin/env python

from smbus import SMBus
import cwiid
import sys
import os
import time
import re

adc_address1 = 0x68
adc_address2 = 0x69

adcreading = bytearray()

adcreading.append(0x00)
adcreading.append(0x00)
adcreading.append(0x00)
adcreading.append(0x00)

varDivisior = 1 # from pdf sheet on adc addresses and config
varMultiplier = (2.4705882/varDivisior)/1000

# detect i2C port number and assign to i2c_bus
for line in open('/proc/cpuinfo').readlines():
    m = re.match('(.*?)\s*:\s*(.*)', line)
    if m:
        (name, value) = (m.group(1), m.group(2))
        if name == "Revision":
            if value [-4:] in ('0002', '0003'):
                i2c_bus = 0
            else:
                i2c_bus = 1
            break
               

bus = SMBus(i2c_bus)
 

def connect_wiimote():
	print 'Put Wiimote in discoverable mode now (press 1+2)...'
	global wiimote
	while True:
		try:
			wiimote = cwiid.Wiimote('00:1F:C5:47:E4:F1')#add address of Wiimote here for speedup)
			break
		except:
			continue
	#Set Wiimote options
	global led
	print "connected"
	led = True
	time.sleep(1)
	for i in range(15, 0):
		wiimote.led = i
		time.sleep(1)

	wiimote.led = 0
	wiimote.rpt_mode = cwiid.RPT_BTN
	wiimote.enable(cwiid.FLAG_MESG_IFC)

def changechannel(address, adcConfig):
	tmp= bus.write_byte(address, adcConfig)

def getadcreading(address, adcConfig):
	adcreading = bus.read_i2c_block_data(address,adcConfig)
	h = adcreading[0]
	l = adcreading[1]
	s = adcreading[2]
	
	# wait for new data
	while (s & 128):
		adcreading = bus.read_i2c_block_data(address,adcConfig)
		h = adcreading[0]
		l = adcreading[1]
		s = adcreading[2]
		
	
	# shift bits to product result
	t = (h << 8) | l
	# check if positive or negative number and invert if needed
	if (h > 128):
		t = ~(0x020000 - t)
	return t * varMultiplier
	
global wiimote
connect_wiimote()

values = [0.0, 0.0, 0.0, 0.0]

while True:
	changechannel(adc_address1, 0x90)
	values[0] = getadcreading(adc_address1,0x90)
	changechannel(adc_address1, 0xB0)
	values[1] = getadcreading(adc_address1,0xB0)
	changechannel(adc_address1, 0xD0)
	values[2] = getadcreading(adc_address1,0xD0)
	changechannel(adc_address1, 0xF0)
	values[2] = getadcreading(adc_address1,0xF0)
	changechannel(adc_address2, 0x90)
	values[3] = getadcreading(adc_address2,0x90)

	led = 0	
	for i in range(0, 4):
		if ( values[i] > 1):
			led += 2**i
	
	wiimote.led = led
	

wiimote.close()
