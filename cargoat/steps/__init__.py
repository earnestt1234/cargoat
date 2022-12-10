# -*- coding: utf-8 -*-
'''cargoat!'''

__all__ = [
    'AddDoors',
    'Close',
    'Finish',
    'IfElse',
    'InitDoorsFixed',
    'InitDoorsRandom',
    'Pick',
    'PlaceCar',
    'RearrangeDoors',
    'RemoveCar',
    'RemoveDoors',
    'Reveal',
    'Stay',
    'Switch',
    'UnPick'
    ]

from cargoat.steps.car import PlaceCar, RemoveCar
from cargoat.steps.pick import Pick, UnPick
from cargoat.steps.reveal import Reveal, Close

from cargoat.steps.convenience import Stay, Switch

from cargoat.steps.initialization import InitDoorsFixed, InitDoorsRandom

from cargoat.steps.logical import IfElse

from cargoat.steps.remodeling import AddDoors, RemoveDoors, RearrangeDoors

from cargoat.steps.results import Finish

