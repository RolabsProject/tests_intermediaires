#!/usr/bin/env python
# read abelectronics ADC Pi V2 board inputs with repeating reading from each channel.
# 12 bit data rate
# # Requries Python 2.7
# Requires SMBus 
# I2C API depends on I2C support in the kernel

# Version 1.0  - 18/01/2014
# Version History:
# 1.0 - Initial Release

#
# Usage: changechannel(address, hexvalue) to change to new channel on adc chips
# Usage: getadcreading(address, hexvalue) to return value in volts from selected channel.
#
# address = adc_address1 or adc_address2 - Hex address of I2C chips as configured by board header pins.

from smbus import SMBus
import re

adc_address1 = 0x68
adc_address2 = 0x69

# create byte array and fill with initial values to define size
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
	
while True:
	changechannel(adc_address1, 0x90)
	print ("Channel 1: %02f" % getadcreading(adc_address1,0x90)), "\t",
	changechannel(adc_address1, 0xB0)
	print ("Channel 2: %02f" % getadcreading(adc_address1,0xB0)), "\t",
	changechannel(adc_address1, 0xD0)
	print ("Channel 3 :%02f" % getadcreading(adc_address1,0xD0)), "\t",
	changechannel(adc_address1, 0xF0)
	print ("Channel 4: %02f" % getadcreading(adc_address1,0xF0)), "\t",
	changechannel(adc_address2, 0x90)
	print ("Channel 5: %02f" % getadcreading(adc_address2,0x90)), "\t"
	#changechannel(adc_address2, 0xB0)
	#print ("Channel 6: %02f" % getadcreading(adc_address2,0xB0)), "\t",
	#changechannel(adc_address2, 0xD0)
	#print ("Channel 7 :%02f" % getadcreading(adc_address2,0xD0)), "\t",
	#changechannel(adc_address2, 0xF0)
	#print ("Channel 8: %02f" % getadcreading(adc_address2,0xF0)), "\t"
