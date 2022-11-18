#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 20:37:53 2022

@author: earnestt1234
"""

from cargoat.steps.generic import GenericAction

class Reveal(GenericAction):
    def __init__(self, doors=1, weighted=False, exclude_current=True,
                 exclude_cars=True, exclude_picked=True,
                 allow_spoiled=False, allow_redundant=True):
        super().__init__(target='revealed',
                         doors=doors,
                         weighted=weighted,
                         behavior='add',
                         exclude_picked=exclude_picked,
                         exclude_revealed=exclude_current,
                         exclude_cars=exclude_cars,
                         allow_redundant=allow_redundant,
                         allow_spoiled=allow_spoiled)

class Close(GenericAction):
    def __init__(self, doors=1, weighted=False, exclude_current=True,
                 allow_spoiled=False, allow_redundant=True):
        super().__init__(target='revealed',
                         doors=doors,
                         weighted=weighted,
                         behavior='remove',
                         exclude_closed=exclude_current,
                         allow_redundant=allow_redundant,
                         allow_spoiled=allow_spoiled)
