# -*- coding: utf-8 -*-
'''cargoat!'''

# load the version (and remove from namespace)
from ._version import v
__version__ = v
del v

# imports
from .core import simulate
from .steps.close import Close
from .steps.pick import Pick
from .steps.reveal import Reveal
