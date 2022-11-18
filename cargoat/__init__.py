# -*- coding: utf-8 -*-
'''cargoat!'''

# load the version (and remove from namespace)
from ._version import v
__version__ = v
del v

__all__ = [
    'PlaceCar',
    'RemoveCar',
    'Pick',
    'UnPick',
    'Reveal',
    'Close',
    'InitDoorsFixed',
    'InitDoorsRandom',
    'AddDoors',
    'RemoveDoors',
    'RearrangeDoors',
    'Finish',
    'simulate'
    ]

# imports
from cargoat.core import simulate
from cargoat.steps import (
    PlaceCar,
    RemoveCar,
    Pick,
    UnPick,
    Reveal,
    Close,
    InitDoorsFixed,
    InitDoorsRandom,
    AddDoors,
    RemoveDoors,
    RearrangeDoors,
    Finish
    )


