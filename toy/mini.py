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
from enum import IntEnum
from functools import partialmethod, lru_cache

from sphero_unsw.commands.api_and_shell import ApiAndShell
from sphero_unsw.commands.connection import Connection
from sphero_unsw.commands.drive import Drive
from sphero_unsw.commands.factory_test import FactoryTest
from sphero_unsw.commands.firmware import Firmware
from sphero_unsw.commands.io import IO
from sphero_unsw.commands.power import Power
from sphero_unsw.commands.sensor import Sensor
from sphero_unsw.commands.system_info import SystemInfo
from sphero_unsw.commands.system_mode import SystemMode
from sphero_unsw.controls.v2 import DriveControl, FirmwareUpdateControl, LedControl, SensorControl, \
    StatsControl
from sphero_unsw.toy import ToyV2, Toy, ToySensor
from sphero_unsw.types import ToyType


class Mini(ToyV2):
    toy_type = ToyType('Sphero Mini', 'SM-', 'SM', .12)
    _handshake = [('00020005-574f-4f20-5370-6865726f2121', bytearray(b'usetheforce...band'))]  # Remove ForceBand

    class LEDs(IntEnum):
        AIMING = 0
        BODY_RED = 1
        BODY_GREEN = 2
        BODY_BLUE = 3
        USER_BODY_RED = 4
        USER_BODY_GREEN = 5
        USER_BODY_BLUE = 6

    # Sensors Available:
    sensors = OrderedDict(
        quaternion=OrderedDict(
            x=ToySensor(0x2000000, -1., 1.),
            y=ToySensor(0x1000000, -1., 1.),
            z=ToySensor(0x800000, -1., 1.),
            w=ToySensor(0x400000, -1., 1.)
        ),
        attitude=OrderedDict(
            pitch=ToySensor(0x40000, -179., 180.),
            roll=ToySensor(0x20000, -179., 180.),
            yaw=ToySensor(0x10000, -179., 180.)
        ),
        accelerometer=OrderedDict(
            x=ToySensor(0x8000, -8.19, 8.19),
            y=ToySensor(0x4000, -8.19, 8.19),
            z=ToySensor(0x2000, -8.19, 8.19)
        ),
        accel_one=OrderedDict(accel_one=ToySensor(0x200, 0., 8000.)),
        locator=OrderedDict(
            x=ToySensor(0x40, -32768., 32767., lambda x: x * 100.),
            y=ToySensor(0x20, -32768., 32767., lambda x: x * 100.),
        ),
        velocity=OrderedDict(
            x=ToySensor(0x10, -32768., 32767., lambda x: x * 100.),
            y=ToySensor(0x8, -32768., 32767., lambda x: x * 100.),
        ),
        speed=OrderedDict(speed=ToySensor(0x4, 0., 32767.)),
        core_time=OrderedDict(core_time=ToySensor(0x2, 0., 0.))
    )

    extended_sensors = OrderedDict(
        gyroscope=OrderedDict(
            x=ToySensor(0x2000000, -20000., 20000.),
            y=ToySensor(0x1000000, -20000., 20000.),
            z=ToySensor(0x800000, -20000., 20000.)
        )
    )

    # Mini Supported calls
    # API and Shell:
    ping = ApiAndShell.ping  # PingCommand
    get_api_protocol_version = ApiAndShell.get_api_protocol_version  # GetApiProtocolVersionCommand
    send_command_to_shell = ApiAndShell.send_command_to_shell  # SendCommandToShellCommand
    add_send_string_to_console_listener = partialmethod(Toy._add_listener,
                                                        ApiAndShell.send_string_to_console)  # SendStringToConsoleCommand
    remove_send_string_to_console_listener = partialmethod(Toy._remove_listener,
                                                           ApiAndShell.send_string_to_console)  # SendStringToConsoleCommand

    # Connection
    get_bluetooth_name = Connection.get_bluetooth_name  # GetBluetoothNameCommand
    set_bluetooth_name = Connection.set_bluetooth_name  # SetBluetoothNameCommand

    # Drive
    set_raw_motors = Drive.set_raw_motors  # SetRawMotorsCommand
    reset_yaw = Drive.reset_yaw  # ResetYawCommand
    drive_with_heading = Drive.drive_with_heading  # DriveWithHeadingCommand
    set_stabilization = Drive.set_stabilization  # SetStabilizationCommand

    # FactoryTest
    exit_factory_mode = FactoryTest.exit_factory_mode  # ExitFactoryModeCommand
    get_chassis_id = FactoryTest.get_chassis_id  # GetChassisIdCommand

    # Firmware
    get_pending_update_flags = Firmware.get_pending_update_flags  # GetPendingUpdateFlagsCommand

    # IO
    set_all_leds_with_16_bit_mask = IO.set_all_leds_with_16_bit_mask  # SetAllLedsWith16BitMaskCommand
    start_idle_led_animation = IO.start_idle_led_animation  # StartIdleLedAnimationCommand

    # Power
    add_battery_state_changed_notify_listener = partialmethod(Toy._add_listener,
                                                              Power.battery_state_changed_notify)  # BatteryStateChangedNotifyCommand
    remove_battery_state_changed_notify_listener = partialmethod(Toy._remove_listener,
                                                                 Power.battery_state_changed_notify)  # BatteryStateChangedNotifyCommand
    add_did_sleep_notify_listener = partialmethod(Toy._add_listener,
                                                  Power.did_sleep_notify)  # DidSleepNotifyCommand
    remove_did_sleep_notify_listener = partialmethod(Toy._remove_listener,
                                                     Power.did_sleep_notify)  # DidSleepNotifyCommand
    add_will_sleep_notify_listener = partialmethod(Toy._add_listener,
                                                   Power.will_sleep_notify)  # WillSleepNotifyCommand
    remove_will_sleep_notify_listener = partialmethod(Toy._remove_listener,
                                                      Power.will_sleep_notify)  # WillSleepNotifyCommand
    enable_battery_state_changed_notify = Power.enable_battery_state_changed_notify  # EnableBatteryStateChangedNotifyCommand
    enter_deep_sleep = Power.enter_deep_sleep  # EnterDeepSleepCommand
    get_battery_percentage = Power.get_battery_percentage  # GetBatteryPercentageCommand
    get_battery_state = Power.get_battery_state  # GetBatteryStateCommand
    get_battery_voltage = Power.get_battery_voltage  # GetBatteryVoltageCommand
    get_battery_voltage_state = Power.get_battery_voltage_state  # GetBatterVoltageCommand
    sleep = Power.sleep  # SleepCommand
    wake = Power.wake  # WakeCommand

    # Sensor
    add_collision_detected_notify_listener = partialmethod(Toy._add_listener,
                                                           Sensor.collision_detected_notify)  # CollisionDetectedNotifyCommand
    remove_collision_detected_notify_listener = partialmethod(Toy._remove_listener,
                                                              Sensor.collision_detected_notify)  # CollisionDetectedNotifyCommand
    configure_collision_detection = Sensor.configure_collision_detection  # ConfigureCollisionDetectionCommand
    enable_collision_detected_notify = Sensor.enable_collision_detected_notify  # EnableCollisionDetectedNotifyCommand
    enable_gyro_max_notify = Sensor.enable_gyro_max_notify  # EnableGyroMaxNotifyCommand
    get_extended_sensor_streaming_mask = Sensor.get_extended_sensor_streaming_mask  # GetExtendedSensorStreamingMaskCommand
    set_extended_sensor_streaming_mask = Sensor.set_extended_sensor_streaming_mask  # SetExtendedSensorStreamingMaskCommand
    get_sensor_streaming_mask = Sensor.get_sensor_streaming_mask  # SetSensorStreamingMaskCommand
    set_sensor_streaming_mask = Sensor.set_sensor_streaming_mask  # GetSensorStreamingMaskCommand
    add_gyro_max_notify_listener = partialmethod(Toy._add_listener, Sensor.gyro_max_notify)  # GyroMaxNotifyCommand
    remove_gyro_max_notify_listener = partialmethod(Toy._remove_listener,
                                                    Sensor.gyro_max_notify)  # GyroMaxNotifyCommand
    reset_locator_x_and_y = Sensor.reset_locator_x_and_y  # ResetLocationXAndYCommand
    add_sensor_streaming_data_notify_listener = partialmethod(Toy._add_listener,
                                                              Sensor.sensor_streaming_data_notify)  # SensorStreamingDataNotifyCommand
    remove_sensor_streaming_data_notify_listener = partialmethod(Toy._remove_listener,
                                                                 Sensor.sensor_streaming_data_notify)  # SensorStreamingDataNotifyCommand
    set_locator_flags = Sensor.set_locator_flags  # SetLocatorFlagsCommand

    # System Info
    get_board_revision = SystemInfo.get_board_revision  # GetBoardRevisionCommand
    get_bootloader_version = SystemInfo.get_bootloader_version  # GetBootloaderVersionCommand
    get_mac_address = SystemInfo.get_mac_address  # GetMacAddressCommand
    get_main_app_version = SystemInfo.get_main_app_version  # GetMainAppVersionCommand
    get_model_number = SystemInfo.get_model_number  # GetModelNumberCommand
    get_processor_name = SystemInfo.get_processor_name  # GetProcessorNameCommand
    get_stats_id = SystemInfo.get_stats_id  # GetStatsIdCommand
    get_three_character_sku = SystemInfo.get_three_character_sku  # GetThreeCharacterSkuCommand

    # System Mode
    enable_desktoy_mode = SystemMode.enable_desktoy_mode  # EnableDesktoyModeCommand

    # Controls - V2
    @property
    @lru_cache(None)
    def drive_control(self):
        return DriveControl(self)

    @property
    @lru_cache(None)
    def multi_led_control(self):
        return LedControl(self)

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
