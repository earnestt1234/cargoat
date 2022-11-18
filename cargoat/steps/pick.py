#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 08:52:01 2022

@author: earnestt1234
"""

from cargoat.steps.generic import GenericAction

class Pick(GenericAction):
    def __init__(self, doors=1, weighted=False, exclude_current=True,
                 exclude_revealed=True, add=False, allow_spoiled=False,
                 allow_redundant=True):
        behavior = 'add' if add else 'overwrite'
        super().__init__(target='picked',
                         doors=doors,
                         weighted=weighted,
                         behavior=behavior,
                         exclude_picked=exclude_current,
                         exclude_revealed=exclude_revealed,
                         allow_redundant=allow_redundant,
                         allow_spoiled=allow_spoiled)

class UnPick(GenericAction):
    def __init__(self, doors=1, weighted=False, exclude_current=True,
                 allow_spoiled=False, allow_redundant=True):
        super().__init__(target='picked',
                         doors=doors,
                         weighted=weighted,
                         behavior='remove',
                         exclude_unpicked=exclude_current,
                         allow_redundant=allow_redundant,
                         allow_spoiled=allow_spoiled)
