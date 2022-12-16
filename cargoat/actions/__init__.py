# -*- coding: utf-8 -*-

'''This subpackage defines classes for Monty Hall game actions,
such as picking doors, revealing doors, etc.  The classes should be
instantiated when defining games passed to `cargoat.core.play()`.'''

__all__ = [
    'AddDoors',
    'ChanceTo',
    'CheckSpoiled',
    'Close',
    'Finish',
    'IfElse',
    'InitDoorsEmpty',
    'InitDoorsFixed',
    'InitDoorsRandom',
    'MarkSpoiled',
    'MarkUnspoiled',
    'Pass',
    'Pick',
    'PlaceCar',
    'RearrangeDoors',
    'RemoveCar',
    'RemoveDoors',
    'Reveal',
    'Stay',
    'Switch',
    'TryExcept',
    'Unpick'
    ]

from cargoat.actions.car import PlaceCar, RemoveCar
from cargoat.actions.pick import Pick, Unpick
from cargoat.actions.reveal import Reveal, Close

from cargoat.actions.convenience import Pass, Stay, Switch

from cargoat.actions.initialization import (InitDoorsEmpty,
                                            InitDoorsFixed,
                                            InitDoorsRandom)

from cargoat.actions.logical import ChanceTo, IfElse, TryExcept

from cargoat.actions.remodeling import AddDoors, RemoveDoors, RearrangeDoors

from cargoat.actions.results import Finish

from cargoat.actions.spoiling import CheckSpoiled, MarkSpoiled, MarkUnspoiled

