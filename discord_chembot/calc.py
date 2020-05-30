
#!/usr/bin/python3
################################################################################
## Chemical element resource database from wikipedia/mendeleev python library ##
##                             for discord bot                                ##
################################################################################
# Copyright (c) 2020 Adam Galindo                                             ##
#                                                                             ##
# Permission is hereby granted, free of charge, to any person obtaining a copy##
# of this software and associated documentation files (the "Software"),to deal##
# in the Software without restriction, including without limitation the rights##
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell   ##
# copies of the Software, and to permit persons to whom the Software is       ##
# furnished to do so, subject to the following conditions:                    ##
#                                                                             ##
# Licenced under GPLv3                                                        ##
# https://www.gnu.org/licenses/gpl-3.0.en.html                                ##
#                                                                             ##
# The above copyright notice and this permission notice shall be included in  ##
# all copies or substantial portions of the Software.                         ##
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
####
################################################################################
##    Search by element number, symbol,
##    list resources available
##    TODO: show basic info if no specificity in query
# created by : mr_hai on discord / flyingfishfuse on github
## Test/Personal Server : https://discord.gg/95V7Mn
import sys
import asyncio
import discord
import math, cmath
from discord.ext import commands
from chempy import balance_stoichiometry, mass_fractions


class LC_circuit():
    def __init__(self, inductance, capacitance, voltage, current = 0,  series = 1, parallel = 0):
        '''
        LC circuit calculator.
            LC_circuit(inductance , capactitance, voltage, current = 0, series = 1, parallel = 0)
        REQUIRED parameters are inductance, capacitance, and voltage.
        '''
        self.inductance               = inductance
        self.capacitance              = capacitance
        self.voltage                  = voltage
        self.current                  = current
        self.resonant_frequency_hertz = 1/(2 * pi * math.sqrt(self.inductance * self.capacitance))
        self.resonant_frequency_w     = math.sqrt(1/(self.inductance * self.capacitance))
        if series:
            self.impedance            = ((math.pow(self.resonant_frequency_w , 2) * self.inductance * self.capacitance - 1)* 1j) / (self.resonant_frequency_w * self.capacitance)
        elif parallel:
            self.impedance            = (-1j * self.resonant_frequency_w * self.inductance)/ (math.pow(self.resonant_frequency_w , 2) * self.inductance * self.capacitance -1)
        else:
            print("AGGGGHHHHH MY LC_circuit IS BURNING AGHHHHHHH!!!")

class Transistor_NPN():
    def __init__ (gain , current_in, voltage_in,frequency, resistor1, resistor2, resistor3):
        '''
        Transistor_NPN(gain,current_in, voltage_in, frequency, res1, res2, res3))
        The resistors are as follows, r1 is collector, r2 is base, r3 is emitter
        REQUIRED parameters are current, voltage, resistors 1-3
        '''

        self.gain           = gain
        self.current_in     = current_in
        self.voltage_in     = voltage_in
        self.DCcurrentGain  = self.collectorcurrent / self.basecurrent
        self.emitteralpha   = self.collectorcurrent / self.emittercurrent
        self.resistor1      = Resistor(resistor1) # collector
        self.resistor2      = Resistor(resistor2) # base
        self.resistor3      = Resistor(resistor3) # emitter
        self.basecurrent    = (voltage_in - Vbe) / self.resistor2.resistance
        self.emittercurrent = (voltage_in - Vbe) / (self.resistor2.resistance/gain)





class RLC_circuit:
    def _init_(self, resistance, inductance, capacitance, voltage, current, frequency ):

        self.resistance               = resistance
        self.inductance               = inductance
        self.capacitance              = capacitance
        self.voltage                  = voltage
        self.current                  = current
        self.resonant_frequency_w = 2 * pi * frequency
        if series:
            self.attenuation = self.resistance / 2 * self.inductance
            self.resonant_frequency = 1/(math.sqrt(self.inductance * self.capacitance))
            self.damping_factor = (self.resistance/2) * (math.sqrt(self.capacitance * self.inductance))
            self.q_factor = 1/self.resistance * math.sqrt(self.inductance/self.capacitance)
            self.bandwidth = 2 * self.attenuation / self.resonant_frequency
            if self.damping_factor < 1:
                self.underdamped = 1
            elif self.damping_factor > 1:
                self.overdamped = 1
            else:
                print "you managed to make a number that is neither greater than or less than or even equal to 1 ... GOOD JOB!"
        elif parallel:
            self.attenuation = 1 / (2 * self.resistance * self.capacitance)
            self.damping_factor = (1/(2 * self.resistance))* math.sqrt(self.inductance / self.capacitance)
            self.q_factor = self.resistance * math.sqrt(self.capacitance/self.inductance)
            self.bandwidth = (1/ self.resistance) * math.sqrt(self.inductance/self.capacitance)
            self.frequency_domain = 1/(1j * self.resonant_frequency * self.inductance) + 1j * self.resonant_frequency * self.capacitance + 1/self.resistance
            if self.damping_factor < 1:
                self.underdamped = 1
            elif self.damping_factor > 1:
                self.overdamped = 1
            else:
                print "you managed to make a number that is neither greater than or less than or even equal to 1 ... GOOD JOB!"

class Resistor:
    def __init__ (self, resistance, current, voltage):
        self.resistance   = resistance
        self.voltage      = voltage
        self.current      = self.voltage / self.resistance
        self.resistance   = self.voltage / self.current
        self.voltage      = self.resistance * self.current
        self.loss         = self.voltage^2 / self.resistance


class Inductor:
    def __init__ (self, inductance, current, voltage, frequency = 0):
        self.inductance   = inductance
        self.current      = current
        self.voltage      = voltage
        self.frequency    = frequency
        self.stored_e     = 1/2 * (inductance * current^2)
        self.qfactor      = (2 * pi * self.frequency * self.inductance) / self.resistance


class Capacitor:
    def __init__(self, capacitance, voltage, frequency):
        self.capacitance    = capacitance
        self.voltage        = voltage
        self.frequency      = frequency
        self.charge_ratio   = self.capacitance * self.voltage
        self.efield_energy  = 1/2 * voltage * self.charge_ratio
        self.reactance      = -(1/(2 * pi * self.frequency * self.capacitance))
        self.impedance      = -(1j/(2 * pi * self.frequency * self.capacitance))



class RL_Circuit:
    def __init__(self, resistance , inductance , frequency, voltage_in, series = 1, parallel = 0 ):
        self.resistance        = resistance
        self.inductance        = inductance
        self.frequency         = frequency
        self.voltage_in        = voltage_in
        self.complex_frequency = 1j * (2 * pi * self.frequency)
        self.complex_impedance = self.inductance * self.complex_frequency


#    def _init_(self, number, unit):
#        self.unit = unit
#        self.number = number
#        if unit == "mega":
#            return self.number*self.mega
#        elif self.unit == "kilo":
#            return self.number*self.kilo
#        elif self.unit == "hecto":
#            return self.number*self.hecto
#        elif self.unit == "deca":
#            return self.number*self.deca
#        elif self.unit == "deci":
#            return self.number*self.deci
#        elif self.unit == "milli":
#            return self.number*self.milli
#        elif self.unit == "micro":
#            return self.number*self.micro
#        elif self.unit == "pico":
#            return self.number*self.pico
#        elif self.unit == "nano":
#            return self.number*self.nano
#        else:
#            print "converter function is not designed for bananas or units measuring bananas or bacon"