# -*- coding: utf-8 -*-
'''cargoat!'''

# load the version (and remove from namespace)
from ._version import v
__version__ = v
del v

__all__ = [
    'AddDoors',
    'ChanceTo',
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
    'TryExcept',
    'UnPick',
    'simulate'
    ]

# imports
from cargoat.core import simulate
from cargoat.steps import (
    AddDoors,
    ChanceTo,
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
    TryExcept,
    UnPick,
    )


