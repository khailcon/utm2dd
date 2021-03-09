"""Translate UTM strings into Decimal Degrees.

This module builds off the utm package to translate batches of UTM coordinates into latitude and longitude coordinates. 

This module works with UTM coordines formatted as follows: "10M 551884.29mE 5278575.64mN"
Digits can by of any length.

"""
from .utm2dd import *