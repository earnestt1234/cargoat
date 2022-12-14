# -*- coding: utf-8 -*-
'''Cargoat is a Python package for simulating Monty Hall type games.'''

# load the version (and remove from namespace)
from ._version import v
__version__ = v
del v

__all__ = [
    'AddDoors',
    'ChanceTo',
    'CheckSpoiled',
    'Close',
    'Finish',
    'IfElse',
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
    'Unpick',
    'play'
    ]

# imports
from cargoat.core import play
from cargoat.sim import MontyHallSim, combine_sims
from cargoat.steps import (
    AddDoors,
    ChanceTo,
    CheckSpoiled,
    Close,
    Finish,
    IfElse,
    InitDoorsFixed,
    InitDoorsRandom,
    MarkSpoiled,
    MarkUnspoiled,
    Pass,
    Pick,
    PlaceCar,
    RearrangeDoors,
    RemoveCar,
    RemoveDoors,
    Reveal,
    Stay,
    Switch,
    TryExcept,
    Unpick,
    )


