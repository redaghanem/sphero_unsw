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

from collections import OrderedDict
from functools import partialmethod, lru_cache

from sphero_unsw.commands.async_ import Async
from sphero_unsw.commands.bootloader import Bootloader
from sphero_unsw.commands.core import Core
from sphero_unsw.commands.sphero import Sphero as SpheroCmd
from sphero_unsw.controls.v1 import DriveControl, SensorControl, StatsControl, FirmwareUpdateControl
from sphero_unsw.toy import ToySensor, Toy
from sphero_unsw.types import ToyType


class Sphero(Toy):
    toy_type = ToyType('SPRK/2.0', None, 'Sphero', .06)

    sensors = OrderedDict(
        attitude=OrderedDict(
            pitch=ToySensor(0x40000, -179., 180.),
            roll=ToySensor(0x20000, -179., 180.),
            yaw=ToySensor(0x10000, -179., 180.)
        ),
        accelerometer=OrderedDict(
            x=ToySensor(0x8000, -32768., 32767., lambda x: x / 4096),
            y=ToySensor(0x4000, -32768., 32767., lambda x: x / 4096),
            z=ToySensor(0x2000, -32768., 32767., lambda x: x / 4096)
        ),
        gyroscope=OrderedDict(
            x=ToySensor(0x1000, -20000., 20000., lambda x: x * .1),
            y=ToySensor(0x800, -20000., 20000., lambda x: x * .1),
            z=ToySensor(0x400, -20000., 20000., lambda x: x * .1)
        ),
        back_emf=OrderedDict(
            left=ToySensor(0x40, -32768., 32767.),
            right=ToySensor(0x20, -32768., 32767.),
        )
    )

    extended_sensors = OrderedDict(
        quaternion=OrderedDict(
            x=ToySensor(0x80000000, -10000., 10000., lambda x: x / 10000),
            y=ToySensor(0x40000000, -10000., 10000., lambda x: x / 10000),
            z=ToySensor(0x20000000, -10000., 10000., lambda x: x / 10000),
            w=ToySensor(0x10000000, -10000., 10000., lambda x: x / 10000)
        ),
        locator=OrderedDict(
            x=ToySensor(0x8000000, -32768., 32767.),
            y=ToySensor(0x4000000, -32768., 32767.),
        ),
        accel_one=OrderedDict(accel_one=ToySensor(0x2000000, 0., 8000.)),
        velocity=OrderedDict(
            x=ToySensor(0x1000000, -32768., 32767., lambda x: x * .1),
            y=ToySensor(0x800000, -32768., 32767., lambda x: x * .1),
        ),
        speed=OrderedDict(speed=ToySensor(0x400000, 0., 32767.)),
    )

    def wake(self):
        self._Toy__adapter.write('22bb746f-2bbf-7554-2d6f-726568705327', bytearray([1]))

    # Async
    add_battery_state_changed_notify_listener = partialmethod(Toy._add_listener,
                                                              Async.battery_state_changed_notify)
    remove_battery_state_changed_notify_listener = partialmethod(Toy._remove_listener,
                                                                 Async.battery_state_changed_notify)
    add_collision_detected_notify_listener = partialmethod(Toy._add_listener,
                                                           Async.collision_detected_notify)
    remove_collision_detected_notify_listener = partialmethod(Toy._remove_listener,
                                                              Async.collision_detected_notify)
    add_did_sleep_notify_listener = partialmethod(Toy._add_listener,
                                                  Async.did_sleep_notify)
    remove_did_sleep_notify_listener = partialmethod(Toy._remove_listener,
                                                     Async.did_sleep_notify)
    add_gyro_max_notify_listener = partialmethod(Toy._add_listener,
                                                 Async.gyro_max_notify)
    remove_gyro_max_notify_listener = partialmethod(Toy._remove_listener,
                                                    Async.gyro_max_notify)
    add_sensor_streaming_data_notify_listener = partialmethod(Toy._add_listener,
                                                              Async.sensor_streaming_data_notify)
    remove_sensor_streaming_data_notify_listener = partialmethod(Toy._remove_listener,
                                                                 Async.sensor_streaming_data_notify)
    add_will_sleep_notify_listener = partialmethod(Toy._add_listener,
                                                   Async.will_sleep_notify)
    remove_will_sleep_notify_listener = partialmethod(Toy._remove_listener,
                                                      Async.will_sleep_notify)

    # Bootloader
    begin_reflash = Bootloader.begin_reflash
    here_is_page = Bootloader.here_is_page
    jump_to_main = Bootloader.jump_to_main

    # Core
    enable_battery_state_changed_notify = Core.enable_battery_state_changed_notify
    get_bluetooth_info = Core.get_bluetooth_info
    get_charger_state = Core.get_charger_state
    get_power_state = Core.get_power_state
    get_versions = Core.get_versions
    jump_to_bootloader = Core.jump_to_bootloader
    ping = Core.ping
    set_bluetooth_name = Core.set_bluetooth_name
    set_inactivity_timeout = Core.set_inactivity_timeout
    sleep = Core.sleep

    # Sphero
    boost = SpheroCmd.boost
    configure_collision_detection = SpheroCmd.configure_collision_detection
    configure_locator = SpheroCmd.configure_locator
    get_chassis_id = SpheroCmd.get_chassis_id
    get_persistent_options = SpheroCmd.get_persistent_options
    get_temperature = SpheroCmd.get_temperature
    set_temporary_options = SpheroCmd.set_temporary_options
    roll = SpheroCmd.roll
    self_level = SpheroCmd.self_level
    set_back_led_brightness = SpheroCmd.set_back_led_brightness
    set_data_streaming = SpheroCmd.set_data_streaming
    set_heading = SpheroCmd.set_heading
    set_main_led = SpheroCmd.set_main_led
    set_motion_timeout = SpheroCmd.set_motion_timeout
    set_persistent_options = SpheroCmd.set_persistent_options
    set_raw_motors = SpheroCmd.set_raw_motors
    set_rotation_rate = SpheroCmd.set_rotation_rate
    set_stabilization = SpheroCmd.set_stabilization

    # Controls - V1
    @property
    @lru_cache(None)
    def drive_control(self):
        return DriveControl(self)

    # The way utils.py is implemented this doesn't need to be present
    # @property
    # @lru_cache(None)
    # def multi_led_control(self):
    #    return LedControl(self)

    @property
    @lru_cache(None)
    def sensor_control(self):
        return SensorControl(self)

    @property
    @lru_cache(None)
    def stats_control(self):
        return StatsControl(self)

    @property
    @lru_cache(None)
    def firmware_update_control(self):
        return FirmwareUpdateControl(self)
