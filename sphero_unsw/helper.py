"""
# ========================================================================
#  sphero_unsw: Extensions and patches for Sphero BOLT+
#  A fork of the original spherov2 library
#
#  Copyright (c) 2019-2021
#      Hanbang Wang,  https://www.cis.upenn.edu/~hanbangw
#      Elionardo Feliciano
#  Original project: https://github.com/EnotPoloskun/spherov2.py
#
#  library spherov2 was originally created for educational use in CIS 521: 
#  Artificial Intelligence at the University of Pennsylvania, where Sphero 
#  robots are used to help teach the foundations of AI.
#
#
#  This extension was developed by:
#       Kathryn Kasmarik (kathryn.kasmarik@unsw.edu.au)
#       Reda Ghanem (reda.ghanem@unsw.edu.au)
#  From the School of Systems and Computing, UNSW Canberra, to support the Sphero BOLT+ robot.
#
#  This extension has been developed for educational use as part of the course ZEIT1102:
#  Introduction to Programming at the University of New South Wales, Canberra (UNSW Canberra).
#  It is specifically designed to support students in learning programming fundamentals and 
#  introductory robotics concepts through hands-on activities using Sphero BOLT+ robots.
#
#  |---------------------------------------------------------------------|
#  | Version: 0.1.9                                                      |
#  | License: MIT License                                                |
#  | Repository: https://github.com/redaghanem/sphero_unsw               |
#  | Pypi package: https://pypi.org/project/sphero-unsw                  |
#  |---------------------------------------------------------------------|
#
# ========================================================================
"""

from functools import lru_cache

from sphero_unsw.types import Color


def to_int(ba):
    return int.from_bytes(ba, byteorder='big')


def to_bytes(i: int, size):
    return i.to_bytes(size, byteorder='big')


@lru_cache(None)
def nibble_to_byte(high, low):
    return (high << 4) | low


def bound_value(lower, value, upper):
    return min(upper, max(lower, value))


def bound_color(color: Color, default_color: Color):
    return Color(
        r=default_color.r if color.r is None else bound_value(0, color.r, 255),
        g=default_color.g if color.g is None else bound_value(0, color.g, 255),
        b=default_color.b if color.b is None else bound_value(0, color.b, 255)
    )


def packet_chk(payload):
    return 0xff - (sum(payload) & 0xff)
