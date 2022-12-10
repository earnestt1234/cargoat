# -*- coding: utf-8 -*-
'''cargoat!'''

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
    'simulate'
    ]

# imports
from cargoat.core import simulate
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


