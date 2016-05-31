# -*- coding: utf-8 -*-

""" This file is part of B{Domogik} project (U{http://www.domogik.org}).

License
=======

B{Domogik} is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

B{Domogik} is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Domogik. If not, see U{http://www.gnu.org/licenses}.

Plugin purpose
==============

Plugin for rpi GPIO

Implements
==========

class GPIO, GPIOException

@author: tikismoke
@copyright: (C) 2007-2016 Domogik project
@license: GPL(v3)
@organization: Domogik
"""

import traceback
import subprocess
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")


class gpioException(Exception):
    """
    GPIO exception
    """
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr(self.value)


class GPIOclass:
    """
    Get informations about gpio
    """
    # -------------------------------------------------------------------------------------------------
    def __init__(self, log, pinmode):
        try:
	    """
            Create a gpio instance, allowing to use GPIO
            """
            self.log = log
            self.log.info(u"==> GPIO version : %s" % GPIO.VERSION)
            self.log.info(u"==> RPI version : %s" % GPIO.RPI_INFO['P1_REVISION'])
            self.log.info(u"==> RPI type : %s" % GPIO.RPI_INFO['TYPE'])
            self.log.info(u"==> pin mode : %s" % pinmode)
	    if pinmode == "BOARD":
    		GPIO.setmode(GPIO.BOARD)
    	    else:
		    GPIO.setmode(GPIO.BCM)
            self.log.info(u"==> get mode : %s" % GPIO.getmode())
	except ValueError:
	    self.log.error(u"error reading Rpi.GPIO.")
	    return

    # -------------------------------------------------------------------------------------------------
    def readSensor(self, pin):
        """
        Read Pin
        """
        try:
            GPIO.setup(int(pin), GPIO.IN)
	    self.log.info(u"==> Reading input '%s'" % pin)
            value = GPIO.input(int(pin))
            return value
        except AttributeError:
            self.log.error(u"### Sensor '%s', ERROR while reading value." % sensor)
            return "failed"


    # -------------------------------------------------------------------------------------------------
    def writeSensor(self, pin, value):
        """
            Write GPIO 'pin' with 'value'
        """
        try:
            GPIO.setup(int(pin), GPIO.OUT)
            self.log.info(u"==> Writing output '%s'" % pin)
            GPIO.output(int(pin), int(value))
        except AttributeError:
            errorstr = u"### Sensor '%s', ERROR while writing value." % pin
            self.log.error(errorstr)
            return False, errorstr
        return True, None



    # -------------------------------------------------------------------------------------------------
    def loop_read_sensor(self, deviceid, device, pin, send, stop):
        """
        """
	pin=2
        while not stop.isSet():
            val = self.readSensor(pin)
            if val != "failed":
                send(deviceid, val)
            self.log.debug(u"=> '{0}' : wait for {1} seconds".format(device, 1))
            stop.wait(1)

""" Need to add a get action=plugin.stop.do
	GPIO.cleanup()
        self.log.debug(u"GPIO cleaning up")
"""