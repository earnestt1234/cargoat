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

from cargoat.steps.car import PlaceCar, RemoveCar
from cargoat.steps.pick import Pick, Unpick
from cargoat.steps.reveal import Reveal, Close

from cargoat.steps.convenience import Pass, Stay, Switch

from cargoat.steps.initialization import (InitDoorsEmpty,
                                          InitDoorsFixed,
                                          InitDoorsRandom)

from cargoat.steps.logical import ChanceTo, IfElse, TryExcept

from cargoat.steps.remodeling import AddDoors, RemoveDoors, RearrangeDoors

from cargoat.steps.results import Finish

from cargoat.steps.spoiling import CheckSpoiled, MarkSpoiled, MarkUnspoiled

