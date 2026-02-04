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
#  | Version: 0.1.10                                                      |
#  | License: MIT License                                                |
#  | Repository: https://github.com/redaghanem/sphero_unsw               |
#  | Pypi package: https://pypi.org/project/sphero-unsw                  |
#  |---------------------------------------------------------------------|
#
# ========================================================================
"""

from enum import IntEnum
from typing import NamedTuple


class CollisionDetected(NamedTuple):
    acceleration_x: float
    acceleration_y: float
    acceleration_z: float
    x_axis: bool
    y_axis: bool
    power_x: int
    power_y: int
    power_z: int
    speed: int
    time: float


class SensorStreamingMask(NamedTuple):
    interval: int
    packet_count: int
    data_mask: int


class BotToBotInfraredReadings(NamedTuple):
    back_left: bool
    back_right: bool
    front_left: bool
    front_right: bool


class RgbcSensorValues(NamedTuple):
    red: int
    green: int
    blue: int
    clear: int


class ColorDetection(NamedTuple):
    red: int
    green: int
    blue: int
    confidence: int
    color_classification_id: int


class StreamingServiceData(NamedTuple):
    token: int
    sensor_data: bytearray


class MotorCurrent(NamedTuple):
    left_motor_current: float
    right_motor_current: float
    up_time: int


class MotorTemperature(NamedTuple):
    case_temperature: float
    winding_coil_temperature: float


class ThermalProtectionStatus(IntEnum):
    OK = 0
    WARN = 1
    CRITICAL = 2


class MotorThermalProtectionStatus(NamedTuple):
    left_motor_temperature: float
    left_motor_status: ThermalProtectionStatus
    right_motor_temperature: float
    right_motor_status: ThermalProtectionStatus
