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
from sphero_unsw.helper import to_bytes, to_int
from sphero_unsw.listeners.core import Versions, BluetoothInfo, PowerState, PowerStates


class IntervalOptions(IntEnum):
    NONE = 0
    DEEP_SLEEP = 0xffff


class ChargerStates(IntEnum):
    OUT = 0
    IN = 1
    UNKNOWN = 2


class PowerStates(IntEnum):
    UNKNOWN = 0
    CHARGING = 1
    OK = 2
    LOW = 3
    CRITICAL = 4


class Core(Commands):
    _did = 0

    @staticmethod
    def ping(toy, proc=None):
        return Core._encode(toy, 1, proc)

    @staticmethod
    def get_versions(toy, proc=None):
        unpacked = struct.unpack('>8B', toy._execute(Core._encode(toy, 2, proc)).data)
        return Versions(
            record_version=unpacked[0], model_number=unpacked[1], hardware_version_code=unpacked[2],
            main_app_version_major=unpacked[3], main_app_version_minor=unpacked[4],
            bootloader_version='%d.%d' % (unpacked[5] >> 4, unpacked[5] & 0xf),
            orb_basic_version='%d.%d' % (unpacked[6] >> 4, unpacked[6] & 0xf),
            overlay_version='%d.%d' % (unpacked[7] >> 4, unpacked[7] & 0xf),
        )

    @staticmethod
    def set_bluetooth_name(toy, name: bytes, proc=None):
        toy._execute(Core._encode(toy, 16, proc, [*name, 0]))

    @staticmethod
    def get_bluetooth_info(toy, proc=None):
        data = toy._execute(Core._encode(toy, 17, proc)).data.rstrip(b'\0')
        name, *_, address = data.split(b'\0')
        return BluetoothInfo(bytes(name), bytes(address))

    @staticmethod
    def get_power_state(toy, proc=None):
        unpacked = struct.unpack('>2B3H', toy._execute(Core._encode(toy, 32, proc)).data)
        return PowerState(record_version=unpacked[0], state=PowerStates(unpacked[1]), voltage=unpacked[2] / 100,
                          number_of_charges=unpacked[3], time_since_last_charge=unpacked[4])

    @staticmethod
    def enable_battery_state_changed_notify(toy, enable: bool, proc=None):
        toy._execute(Core._encode(toy, 33, proc, [int(enable)]))

    @staticmethod
    def sleep(toy, interval_option: IntervalOptions, unk: int, unk2: int, proc=None):
        return toy._execute(Core._encode(toy, 34, proc, [*to_bytes(interval_option, 2), unk, *to_bytes(unk2, 2)]))

    @staticmethod
    def set_inactivity_timeout(toy, timeout: int, proc=None):
        toy._execute(Core._encode(toy, 37, proc, to_bytes(timeout, 2)))

    @staticmethod
    def get_charger_state(toy, proc=None):
        return ChargerStates(toy._execute(Core._encode(toy, 38, proc)).data[0])

    @staticmethod
    def get_factory_config_block_crc(toy, proc=None):
        return to_int(toy._execute(Core._encode(toy, 39, proc)).data)

    @staticmethod
    def jump_to_bootloader(toy, proc=None):
        toy._execute(Core._encode(toy, 48, proc))
