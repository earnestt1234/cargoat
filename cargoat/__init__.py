# -*- coding: utf-8 -*-
'''cargoat!'''

# load the version (and remove from namespace)
from ._version import v
__version__ = v
del v

__all__ = [
    'AddDoors',
    'Close',
    'Finish',
    'IfElse',
    'InitDoorsFixed',
    'InitDoorsRandom',
    'Pass',
    'Pick',
    'PlaceCar',
    'RearrangeDoors',
    'RemoveCar',
    'RemoveDoors',
    'Reveal',
    'Stay',
    'Switch',
    'UnPick',
    'simulate'
    ]

# imports
from cargoat.core import simulate
from cargoat.steps import (
    AddDoors,
    Close,
    Finish,
    IfElse,
    InitDoorsFixed,
    InitDoorsRandom,
    Pass,
    Pick,
    PlaceCar,
    RearrangeDoors,
    RemoveCar,
    RemoveDoors,
    Reveal,
    Stay,
    Switch,
    UnPick,
    )


