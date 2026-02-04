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

from enum import IntEnum

from sphero_unsw.toy.r2d2 import R2D2
from sphero_unsw.types import ToyType


class R2Q5(R2D2):
    toy_type = ToyType('R2-Q5', 'Q5-', 'Q5', .12)

    class Animations(IntEnum):
        CHARGER_1 = 0
        CHARGER_2 = 1
        CHARGER_3 = 2
        CHARGER_4 = 3
        CHARGER_5 = 4
        CHARGER_6 = 5
        CHARGER_7 = 6
        EMOTE_ALARM = 7
        EMOTE_ANGRY = 8
        EMOTE_ATTENTION = 9
        EMOTE_FRUSTRATED = 10
        EMOTE_DRIVE = 11
        EMOTE_EXCITED = 12
        EMOTE_SEARCH = 13
        EMOTE_SHORT_CIRCUIT = 14
        EMOTE_LAUGH = 15
        EMOTE_NO = 16
        EMOTE_RETREAT = 17
        EMOTE_FIERY = 18
        EMOTE_UNDERSTOOD = 19
        EMOTE_YES = 21
        EMOTE_SCAN = 22
        EMOTE_SURPRISED = 24
        IDLE_1 = 25
        IDLE_2 = 26
        IDLE_3 = 27
        WWM_ANGRY = 31
        WWM_ANXIOUS = 32
        WWM_BOW = 33
        WWM_CONCERN = 34
        WWM_CURIOUS = 35
        WWM_DOUBLE_TAKE = 36
        WWM_EXCITED = 37
        WWM_FIERY = 38
        WMM_FRUSTRATED = 39
        WWM_HAPPY = 40
        WWM_JITTERY = 41
        WWM_LAUGH = 42
        WWM_LONG_SHAKE = 43
        WWM_NO = 44
        WWM_OMINOUS = 45
        WWM_RELIEVED = 46
        WWM_SAD = 47
        WWM_SCARED = 48
        WWM_SHAKE = 49
        WWM_SURPRISED = 50
        WWM_TAUNTING = 51
        WWM_WHISPER = 52
        WWM_YELLING = 53
        WWM_YOOHOO = 54
