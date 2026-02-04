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

import struct
from enum import IntEnum, IntFlag

from sphero_unsw.listeners.async_ import CollisionDetected
from sphero_unsw.listeners.core import PowerStates


class CollisionAxis(IntFlag):
    X_AXIS = 0x1  # 0b1
    Y_AXIS = 0x2  # 0b10


class GyroMaxExceedsFlags(IntFlag):
    X_POSITIVE = 0x1  # 0b1
    X_NEGATIVE = 0x2  # 0b10
    Y_POSITIVE = 0x4  # 0b100
    Y_NEGATIVE = 0x8  # 0b1000
    Z_POSITIVE = 0x10  # 0b10000
    Z_NEGATIVE = 0x20  # 0b100000


class PowerStates(IntEnum):
    UNKNOWN = 0
    CHARGING = 1
    OK = 2
    LOW = 3
    CRITICAL = 4


class Async:
    battery_state_changed_notify = (0xfe, 1), lambda listener, p: listener(PowerStates(p.data[0]))
    sensor_streaming_data_notify = (
        (0xfe, 3), lambda listener, p: listener(list(struct.unpack('>%dh' % (len(p.data) // 2), p.data))))
    will_sleep_notify = (0xfe, 5), lambda listener, _: listener()

    @staticmethod
    def __process(listener, packet):
        unpacked = struct.unpack('>3hB2hBL', packet.data)
        listener(CollisionDetected(acceleration_x=unpacked[0] / 4096, acceleration_y=unpacked[1] / 4096,
                                   acceleration_z=unpacked[2] / 4096, x_axis=bool(unpacked[3] & 1),
                                   y_axis=bool(unpacked[3] & 2), power_x=unpacked[4], power_y=unpacked[5],
                                   speed=unpacked[6], time=unpacked[7] / 1000))

    collision_detected_notify = (0xfe, 7), __process.__func__
    gyro_max_notify = (0xfe, 12), lambda listener, p: listener(p.data[0])
    did_sleep_notify = (0xfe, 20), lambda listener, _: listener()
