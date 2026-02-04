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

import struct
from enum import IntEnum

from sphero_unsw.commands import Commands
from sphero_unsw.helper import to_bytes


class R2DoLegActions(IntEnum):
    UNKNOWN = 0
    THREE_LEGS = 1
    TWO_LEGS = 2
    WADDLE = 3
    TRANSITIONING = 4


class R2LegActions(IntEnum):
    STOP = 0
    THREE_LEGS = 1
    TWO_LEGS = 2
    WADDLE = 3


class SuspensionAnimationModes(IntEnum):
    NON_ACTIVE = 0
    ACTIVE = 1


class Animatronic(Commands):
    _did = 23

    @staticmethod
    def play_animation(toy, animation: IntEnum, proc=None):
        toy._execute(Animatronic._encode(toy, 5, proc, to_bytes(animation, 2)))

    @staticmethod
    def perform_leg_action(toy, leg_action: R2LegActions, proc=None):
        toy._execute(Animatronic._encode(toy, 13, proc, [leg_action]))

    @staticmethod
    def set_head_position(toy, head_position: float, proc=None):
        toy._execute(Animatronic._encode(toy, 15, proc, struct.pack('>f', head_position)))

    play_animation_complete_notify = (23, 17, 0xff)

    @staticmethod
    def get_head_position(toy, proc=None):
        return struct.unpack('>f', toy._execute(Animatronic._encode(toy, 20, proc)).data)[0]

    @staticmethod
    def set_leg_position(toy, leg_position: float, proc=None):
        toy._execute(Animatronic._encode(toy, 21, proc, struct.pack('>f', leg_position)))

    @staticmethod
    def get_leg_position(toy, proc=None):
        return struct.unpack('>f', toy._execute(Animatronic._encode(toy, 22, proc)).data)[0]

    @staticmethod
    def get_leg_action(toy, proc=None):
        return R2DoLegActions(toy._execute(Animatronic._encode(toy, 37, proc)).data[0])

    leg_action_complete_notify = (23, 38, 0xff)

    @staticmethod
    def enable_leg_action_notify(toy, enable: bool, proc=None):
        toy._execute(Animatronic._encode(toy, 42, proc, [int(enable)]))

    @staticmethod
    def stop_animation(toy, proc=None):
        toy._execute(Animatronic._encode(toy, 43, proc))

    @staticmethod
    def enable_idle_animations(toy, enable: bool, proc=None):
        toy._execute(Animatronic._encode(toy, 44, proc, [int(enable)]))

    @staticmethod
    def enable_trophy_mode(toy, enable: bool, proc=None):
        toy._execute(Animatronic._encode(toy, 45, proc, [int(enable)]))

    @staticmethod
    def get_trophy_mode_enabled(toy, proc=None):
        return bool(toy._execute(Animatronic._encode(toy, 46, proc)).data[0])

    @staticmethod
    def enable_head_reset_to_zero_notify(toy, enable: bool, proc=None):
        toy._execute(Animatronic._encode(toy, 57, proc, [int(enable)]))

    head_reset_to_zero_notify = (23, 58, 0xff), lambda listener, _: listener()
