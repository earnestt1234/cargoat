#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 22:10:52 2022

@author: earnestt1234
"""

from cargoat.steps.generic import GenericAction

class PlaceCar(GenericAction):
    def __init__(self, doors=1, weighted=False, exclude_current=True,
                 exclude_revealed=True, allow_spoiled=False,
                 allow_redundant=True):
        super().__init__(target='cars',
                         doors=doors,
                         weighted=weighted,
                         behavior='add',
                         exclude_cars=exclude_current,
                         exclude_revealed=exclude_revealed,
                         allow_redundant=allow_redundant,
                         allow_spoiled=allow_spoiled)

class RemoveCar(GenericAction):
    def __init__(self, doors=1, weighted=False, exclude_current=True,
                 exclude_revealed=True, allow_spoiled=False,
                 allow_redundant=True):
        super().__init__(target='revealed',
                         doors=doors,
                         weighted=weighted,
                         behavior='remove',
                         exclude_carless=exclude_current,
                         allow_redundant=allow_redundant,
                         allow_spoiled=allow_spoiled)
