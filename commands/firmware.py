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

from enum import IntFlag, IntEnum

from sphero_unsw.commands import Commands
from sphero_unsw.helper import to_int


class PendingUpdateFlags(IntFlag):
    NORDIC = 0x1  # 0b1
    ST = 0x2  # 0b10
    ESP2886 = 0x4  # 0b100
    AUDIO = 0x8  # 0b1000
    ANIMATIONS = 0x10  # 0b10000
    ST_BOOTLOADER = 0x20  # 0b100000


class ApplicationIds(IntEnum):
    BOOTLOADER = 0
    MAIN_APP = 1


class MainAppValidaties(IntEnum):
    UNKNOWN = 0
    UNKNOWN_BECAUSE_UPDATE_FLAG_SET = 1
    VALID = 2
    INVALID = 3


class ResetStrategies(IntEnum):
    RESET_INTO_OR_JUMP_TO_MAIN_APP = 1
    RESET_INTO_OR_JUMP_TO_BOOTLOADER = 2


class UpdateMethods(IntEnum):
    REQUIRES_RESET = 0
    MASTER_CONTROLS_UPDATE_FLOW = 1
    IN_MASTER_BOOTLOADER = 2


class Firmware(Commands):
    _did = 29

    @staticmethod
    def get_pending_update_flags(toy, proc=None):
        return PendingUpdateFlags(to_int(toy._execute(Firmware._encode(toy, 13, proc)).data))

    @staticmethod
    def get_current_application_id(toy, proc=None):
        return ApplicationIds(toy._execute(Firmware._encode(toy, 21, proc)).data[0])

    @staticmethod
    def get_all_updatable_processors(toy, proc=None):
        toy._execute(Firmware._encode(toy, 22, proc))

    @staticmethod
    def get_version_for_updatable_processors(toy, proc=None):
        toy._execute(Firmware._encode(toy, 24, proc))

    @staticmethod
    def set_pending_update_for_processors(toy, data, proc=None):  # unknown names
        return ResetStrategies(toy._execute(Firmware._encode(toy, 26, proc, data)).data[0])

    @staticmethod
    def get_pending_update_for_processors(toy, proc=None):
        return toy._execute(Firmware._encode(toy, 27, proc)).data

    @staticmethod
    def reset_with_parameters(toy, strategy, proc=None):
        toy._execute(Firmware._encode(toy, 28, proc, [strategy]))

    @staticmethod
    def clear_pending_update_processors(toy, data, proc=None):  # unknown names
        toy._execute(Firmware._encode(toy, 38, proc, data))
