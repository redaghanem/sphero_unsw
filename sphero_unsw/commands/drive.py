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
from enum import IntFlag, IntEnum

from sphero_unsw.commands import Commands
from sphero_unsw.helper import to_bytes
from sphero_unsw.listeners.drive import MotorStall


class DriveFlags(IntFlag):
    FORWARD = 0x0  # 0b0
    BACKWARD = 0x1  # 0b1
    TURBO = 0x2  # 0b10
    FAST_TURN = 0x4  # 0b100
    LEFT_DIRECTION = 0x8  # 0b1000
    RIGHT_DIRECTION = 0x10  # 0b10000
    ENABLE_DRIFT = 0x20  # 0b100000


class RCDriveFlags(IntFlag):
    SLEW_LINEAR_VELOCITY = 0x1  # 0b1


class XYPositionDriveFlags(IntFlag):
    FORCE_REVERSE = 0x1  # 0b1
    AUTO_REVERSE = 0x2  # 0b10


class StabilizationIndexes(IntEnum):
    NO_CONTROL_SYSTEM = 0
    FULL_CONTROL_SYSTEM = 1
    PITCH_CONTROL_SYSTEM = 2
    ROLL_CONTROL_SYSTEM = 3
    YAW_CONTROL_SYSTEM = 4
    SPEED_AND_YAW_CONTROL_SYSTEM = 5


class RawMotorModes(IntEnum):
    OFF = 0
    FORWARD = 1
    REVERSE = 2


class GenericRawMotorIndexes(IntEnum):
    LEFT_DRIVE = 0
    RIGHT_DRIVE = 1
    HEAD = 2
    LEG = 3


class GenericRawMotorModes(IntEnum):
    MOTOR_OFF = 0
    FORWARD = 1
    REVERSE = 2


class LinearVelocitySlewMethods(IntEnum):
    CONSTANT = 0
    PROPORTIONAL = 1


class MotorIndexes(IntEnum):
    LEFT_MOTOR_INDEX = 0
    RIGHT_MOTOR_INDEX = 1


class Drive(Commands):
    _did = 22

    @staticmethod
    def set_raw_motors(toy, left_mode: RawMotorModes, left_speed, right_mode: RawMotorModes, right_speed, proc=None):
        toy._execute(Drive._encode(toy, 1, proc, [left_mode, left_speed, right_mode, right_speed]))

    @staticmethod
    def reset_yaw(toy, proc=None):
        toy._execute(Drive._encode(toy, 6, proc))

    @staticmethod
    def drive_with_heading(toy, speed, heading, drive_flags: DriveFlags, proc=None):
        toy._execute(Drive._encode(toy, 7, proc, [speed, *to_bytes(heading, 2), drive_flags]))

    @staticmethod
    def generic_raw_motor(toy, index: GenericRawMotorIndexes, mode: GenericRawMotorModes, speed, proc=None):
        toy._execute(Drive._encode(toy, 11, proc, [index, mode, *speed]))

    @staticmethod
    def set_stabilization(toy, stabilization_index: StabilizationIndexes, proc=None):
        toy._execute(Drive._encode(toy, 12, proc, [stabilization_index]))

    @staticmethod
    def set_control_system_type(toy, s, s2, proc=None):  # unknown name
        toy._execute(Drive._encode(toy, 14, proc, [s, s2]))

    @staticmethod
    def set_pitch_torque_modification_value(toy, f, proc=None):  # Untested / Unknown Param Name
        toy._execute(Drive._encode(toy, 15, proc, [f]))

    @staticmethod
    def set_component_parameters(toy, s, s2, f_arr, proc=None):  # unknown name
        toy._execute(Drive._encode(toy, 32, proc, [s, s2, *struct.pack('>%df' % len(f_arr), *f_arr)]))

    @staticmethod
    def get_component_parameters(toy, s, s2, proc=None):  # unknown name
        data = toy._execute(Drive._encode(toy, 33, proc, [s, s2])).data
        return struct.unpack('>%df' % (len(data) // 4), data)

    @staticmethod
    def set_custom_control_system_timeout(toy, timeout, proc=None):
        toy._execute(Drive._encode(toy, 34, proc, to_bytes(timeout, 2)))

    @staticmethod
    def enable_motor_stall_notify(toy, enable, proc=None):
        toy._execute(Drive._encode(toy, 37, proc, [int(enable)]))

    motor_stall_notify = (22, 38, 0xff), lambda listener, p: listener(MotorStall(*p.data))

    @staticmethod
    def enable_motor_fault_notify(toy, enable, proc=None):
        toy._execute(Drive._encode(toy, 39, proc, [int(enable)]))

    motor_fault_notify = (22, 40, 0xff), lambda listener, p: listener(bool(p.data[0]))

    @staticmethod
    def get_motor_fault_state(toy, proc=None):
        return bool(toy._execute(Drive._encode(toy, 41, proc)).data[0])
