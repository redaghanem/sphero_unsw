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

import importlib
from functools import partial
from typing import Iterable, List, Type, Callable

from sphero_unsw.commands.sphero import Sphero
from sphero_unsw.toy import Toy
from sphero_unsw.toy.bb8 import BB8
from sphero_unsw.toy.bb9e import BB9E
from sphero_unsw.toy.bolt import BOLT
from sphero_unsw.toy.mini import Mini
from sphero_unsw.toy.ollie import Ollie
from sphero_unsw.toy.r2d2 import R2D2
from sphero_unsw.toy.r2q5 import R2Q5
from sphero_unsw.toy.rvr import RVR
from sphero_unsw.toy.sprk2 import Sprk2
from sphero_unsw.toy.boltplus import BOLTPLUS            # NEW CODE TO SUPPORT BOLTPLUS


class ToyNotFoundError(Exception):
    ...


def all_toys(cls=Toy):
    subtypes = cls.__subclasses__()
    yield cls
    for sub in subtypes:
        yield from all_toys(sub)


def find_toys(*, timeout=5.0, toy_types: Iterable[Type[Toy]] = None,
              toy_names: Iterable[str] = None, adapter=None) -> List[Toy]:
    """Find toys that matches the criteria given.

    :param timeout: Device scanning timeout, in seconds.
    :param toy_types: Iterable of toy types (subclasses of :class:`Toy`) that needs to be scanned. Set to ``None`` to scan
                      all toy types available.
    :param toy_names: Iterable of strings of toy names that needs to be scanned. Set to ``None`` to scan toys with all
                      kinds of names.
    :param adapter: Kind of adapter to use for scanning bluetooth devices. Set to ``None`` to use default
                    :class:`BleakAdapter`.
    :return: A list of toys that are scanned.
    """
    if adapter is None:
        adapter = importlib.import_module(
            'sphero_unsw.adapter.bleak_adapter').BleakAdapter
    if toy_names is not None:
        toy_names = set(toy_names)
    if toy_names is not None and len(toy_names) == 1:
        toy = adapter.scan_toy(list(toy_names)[0], timeout)
        if toy is None:
            return []
        toys = [toy]
    else:
        toys = adapter.scan_toys(timeout)
    if toy_types is None:
        toy_types = set(all_toys())
    ret = []
    for toy in toys:
        if toy.name is None:
            continue
        if toy_names is not None and toy.name not in toy_names:
            continue
        for toy_cls in toy_types:
            toy_type = toy_cls.toy_type
            if toy.name.startswith(toy_type.filter_prefix) and \
                    (toy_type.prefix is None or toy.name.startswith(toy_type.prefix)):
                ret.append(toy_cls(toy, adapter))
                break
    return ret


def find_toy(*, toy_name: str = None, **kwargs) -> Toy:
    """Find a single toy that matches the criteria given.

    :param toy_name: A string of toy name that needs to be scanned. Set to ``None`` to scan toy with all kinds of names.
    :param timeout: Device scanning timeout, in seconds.
    :param toy_types: List of toy types (subclasses of :class:`Toy`) that needs to be scanned. Set to ``None`` to scan
                      all toy types available.
    :param adapter: Kind of adapter to use for scanning bluetooth devices. Set to ``None`` to use default
                    :class:`BleakAdapter`.
    :return: A toy that is scanned.
    :raise ToyNotFoundError: If no toys could be found
    """
    toys = find_toys(toy_names=[toy_name] if toy_name else None, **kwargs)
    if not toys:
        raise ToyNotFoundError
    return toys[0]


find_Sphero: Callable[..., Sphero] = partial(find_toy, toy_types=[Sphero])
find_Ollie: Callable[..., Ollie] = partial(find_toy, toy_types=[Ollie])
find_Mini: Callable[..., Mini] = partial(find_toy, toy_types=[Mini])
find_BB8: Callable[..., BB8] = partial(find_toy, toy_types=[BB8])
find_BB9E: Callable[..., BB9E] = partial(find_toy, toy_types=[BB9E])
find_R2D2: Callable[..., R2D2] = partial(find_toy, toy_types=[R2D2])
find_R2Q5: Callable[..., R2Q5] = partial(find_toy, toy_types=[R2Q5])
find_RVR: Callable[..., RVR] = partial(find_toy, toy_types=[RVR])
find_BOLT: Callable[..., BOLT] = partial(find_toy, toy_types=[BOLT])
find_Sprk2: Callable[..., Sprk2] = partial(find_toy, toy_types=[Sprk2])
find_BOLTPLUS: Callable[..., BOLTPLUS] = partial(find_toy, toy_types=[BOLTPLUS])            # NEW CODE TO SUPPORT BOLTPLUS