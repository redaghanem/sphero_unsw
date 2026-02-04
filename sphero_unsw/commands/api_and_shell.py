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

from sphero_unsw.commands import Commands
from sphero_unsw.listeners.api_and_shell import ApiProtocolVersion


class ApiAndShell(Commands):
    _did = 16

    @staticmethod
    def ping(toy, data, proc=None) -> bytearray:
        return toy._execute(ApiAndShell._encode(toy, 0, proc, data)).data

    @staticmethod
    def get_api_protocol_version(toy, proc=None) -> ApiProtocolVersion:
        data = toy._execute(ApiAndShell._encode(toy, 1, proc)).data
        return ApiProtocolVersion(major_version=data[0], minor_version=data[1])

    @staticmethod
    def send_command_to_shell(toy, command: bytes, proc=None):
        toy._execute(ApiAndShell._encode(toy, 2, proc, [*command, 0]))

    send_string_to_console = (16, 3, lambda listener, p: listener(bytes(p.data).rstrip(b'\0')))

    @staticmethod
    def get_supported_dids(toy, proc=None):
        return list(toy._execute(ApiAndShell._encode(toy, 5, proc)).data)

    @staticmethod
    def get_supported_cids(toy, s, proc=None):
        return list(toy._execute(ApiAndShell._encode(toy, 6, proc, [s])).data)
