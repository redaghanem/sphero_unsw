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

from enum import IntEnum, IntFlag

from sphero_unsw.commands import Commands
from sphero_unsw.helper import to_bytes, to_int
from sphero_unsw.listeners.sphero import Options


class ConfigurationOptions(IntFlag):
    DISABLE_SLEEP_IN_CHARGE = 0x1  # 0b1
    ENABLE_VECTOR_DRIVE = 0x2  # 0b10
    DISABLE_SELF_LEVEL_IN_CHARGER = 0x4  # 0b100
    ENABLE_TAIL_LIGHT_ALWAYS_ON = 0x8  # 0b1000
    ENABLE_MOTION_TIMEOUT = 0x10  # 0b10000
    ENABLE_GYRO_MAX_NOTIFY = 0x100  # 0b100000000
    ENABLE_FULL_SPEED = 0x400  # 0b10000000000


class SelfLevelOptions(IntFlag):
    START = 0x1  # 0b1
    KEEP_HEADING = 0x2  # 0b10
    SLEEP_AFTER = 0x4  # 0b100
    TURN_CONTROL_SYSTEM_ON = 0x8  # 0b1000


class CollisionDetectionMethods(IntEnum):
    OFF = 0
    DEFAULT = 1


class DeviceModes(IntEnum):
    NORMAL = 0
    HACK = 1


class RollModes(IntEnum):
    STOP = 0
    GO = 1
    CALIBRATE = 2


class ReverseFlags(IntEnum):
    OFF = 0
    ON = 1


class RawMotorModes(IntEnum):
    OFF = 0
    FORWARD = 1
    REVERSE = 2
    BRAKE = 3
    IGNORE = 4


class Sphero(Commands):
    _did = 2

    @staticmethod
    def set_heading(toy, heading: int, proc=None):
        toy._execute(Sphero._encode(toy, 1, proc, to_bytes(heading, 2)))

    @staticmethod
    def set_stabilization(toy, stabilize: bool, proc=None):
        toy._execute(Sphero._encode(toy, 2, proc, [int(stabilize)]))

    @staticmethod
    def set_rotation_rate(toy, rate: int, proc=None):
        toy._execute(Sphero._encode(toy, 3, proc, [rate]))

    @staticmethod
    def get_chassis_id(toy, proc=None):
        return to_int(toy._execute(Sphero._encode(toy, 7, proc)).data)

    @staticmethod
    def self_level(toy, opt1: bool, opt2: bool, opt3: bool, opt4: bool, angle_limit, timeout, true_time, proc=None):
        # unknown names
        toy._execute(Sphero._encode(
            toy, 9, proc, [opt1 | (opt2 << 1) | (opt3 << 2) | (opt4 << 3), angle_limit, timeout, true_time]))

    @staticmethod
    def set_data_streaming(toy, interval, num_samples_per_packet, mask, count, extended_mask, proc=None):
        toy._execute(Sphero._encode(
            toy, 17, proc,
            [*to_bytes(interval, 2), *to_bytes(num_samples_per_packet, 2), *to_bytes(mask, 4), count & 0xff,
             *to_bytes(extended_mask, 4)]))

    @staticmethod
    def configure_collision_detection(toy, collision_detection_method: CollisionDetectionMethods,
                                      x_threshold, y_threshold, x_speed, y_speed, dead_time, proc=None):
        toy._execute(Sphero._encode(
            toy, 18, proc, [collision_detection_method, x_threshold, y_threshold, x_speed, y_speed, dead_time]))

    @staticmethod
    def configure_locator(toy, flags, x, y, yaw_tare, proc=None):
        toy._execute(Sphero._encode(toy, 19, proc, [flags, *to_bytes(x, 2), *to_bytes(y, 2), *to_bytes(yaw_tare, 2)]))

    @staticmethod
    def get_temperature(toy, proc=None):
        data = toy._execute(Sphero._encode(toy, 22, proc)).data
        return data[0] + data[1] / 10

    @staticmethod
    def set_main_led(toy, r, g, b, proc=None):
        toy._execute(Sphero._encode(toy, 32, proc, [r, g, b]))

    @staticmethod
    def set_back_led_brightness(toy, brightness, proc=None):
        toy._execute(Sphero._encode(toy, 33, proc, data=[brightness]))

    @staticmethod
    def roll(toy, speed, heading, roll_mode: RollModes, reverse_flag: ReverseFlags, proc=None):
        toy._execute(Sphero._encode(toy, 48, proc, [speed, *to_bytes(heading, 2), roll_mode, reverse_flag]))

    @staticmethod
    def boost(toy, s, s2, proc=None):  # unknown names
        toy._execute(Sphero._encode(toy, 49, proc, [s, *to_bytes(s2, 2)]))

    @staticmethod
    def set_raw_motors(toy, left_mode: RawMotorModes, left_speed, right_mode: RawMotorModes, right_speed, proc=None):
        toy._execute(Sphero._encode(toy, 51, proc, [left_mode, left_speed, right_mode, right_speed]))

    @staticmethod
    def set_motion_timeout(toy, timeout: int, proc=None):
        toy._execute(Sphero._encode(toy, 52, proc, to_bytes(timeout, 2)))

    @staticmethod
    def set_persistent_options(toy, options: Options, proc=None):  # unknown names
        toy._execute(Sphero._encode(toy, 53, proc, to_bytes(
            options.disable_sleep_in_charger | (options.enable_vector_drive << 1) | (
                    options.disable_self_level_in_charger << 2) | (options.enable_tail_light_always_on << 3) | (
                    options.enable_motion_timeout << 4) | (options.enable_gyro_max_notify << 8) | (
                    options.enable_full_speed << 10), 4)))

    @staticmethod
    def get_persistent_options(toy, proc=None):
        data = to_int(toy._execute(Sphero._encode(toy, 54, proc)).data)
        return Options(bool(data & 1), bool(data & 2), bool(data & 4), bool(data & 8), bool(data & 16),
                       bool(data & 256), bool(data & 1024))

    @staticmethod
    def set_temporary_options(toy, options: Options, proc=None):
        toy._execute(Sphero._encode(toy, 55, proc, to_bytes(
            options.disable_sleep_in_charger | (options.enable_vector_drive << 1) | (
                    options.disable_self_level_in_charger << 2) | (options.enable_tail_light_always_on << 3) | (
                    options.enable_motion_timeout << 4) | (options.enable_gyro_max_notify << 8) | (
                    options.enable_full_speed << 10), 4)))

    @staticmethod
    def get_temporary_options(toy, proc=None):
        data = to_int(toy._execute(Sphero._encode(toy, 56, proc)).data)
        return Options(bool(data & 1), bool(data & 2), bool(data & 4), bool(data & 8), bool(data & 16),
                       bool(data & 256), bool(data & 1024))

    @staticmethod
    def get_sku(toy, proc=None):
        return reversed(toy._execute(Sphero._encode(toy, 58, proc)).data)
