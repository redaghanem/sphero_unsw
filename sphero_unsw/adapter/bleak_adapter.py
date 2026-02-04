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

import asyncio
import threading

import bleak


class BleakAdapter:
    @staticmethod
    def scan_toys(timeout: float = 5.0):
        return asyncio.run(bleak.BleakScanner.discover(timeout))

    @staticmethod
    def scan_toy(name: str, timeout: float = 5.0):
        return asyncio.run(
            bleak.BleakScanner.find_device_by_filter(
                lambda _, a: a.local_name == name, timeout))

    def __init__(self, address):
        self.__event_loop = asyncio.new_event_loop()
        self.__device = bleak.BleakClient(address, timeout=5.0)
        self.__lock = threading.Lock()
        self.__thread = threading.Thread(target=self.__event_loop.run_forever)
        self.__thread.start()
        try:
            self.__execute(self.__device.connect())
        except:
            self.close(False)
            raise

    def __execute(self, coroutine):
        with self.__lock:
            return asyncio.run_coroutine_threadsafe(coroutine, self.__event_loop).result()

    def close(self, disconnect=True):
        if disconnect:
            self.__execute(self.__device.disconnect())
        with self.__lock:
            self.__event_loop.call_soon_threadsafe(self.__event_loop.stop)
            self.__thread.join()
        self.__event_loop.close()

    def set_callback(self, uuid, cb):
        self.__execute(self.__device.start_notify(uuid, cb))

    def write(self, uuid, data):
        self.__execute(self.__device.write_gatt_char(uuid, data, True))
