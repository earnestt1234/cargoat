#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 20:37:53 2022

@author: earnestt1234
"""

from cargoat.steps.generic import GenericAction

class Reveal(GenericAction):
    '''Class to model the host opening a door.'''
    def __init__(self, doors=1, weighted=False, exclude_current=True,
                 exclude_cars=True, exclude_picked=True,
                 allow_spoiled=False, allow_redundant=True):
        '''
        Class to model the host revealing one or more doors.
        Revealed doors are signnificant for directing what information
        the player knows, and which further actions are acceptable.

        Parameters
        ----------
        doors : int or list-like, optional
            Argument for specifying how many/which doors to reveal. The default is 1.
            Possible options are as follows:
            - a single integer is interpreted as the number of doors to
            select (randomly, with equal probability)
            - a list of integers with `weighted=False` is interpeted as
            specific doors to pick, e.g. `[0, 2]` selects the doors at
            index 0 and index 2.
            - a list of integers with `weighted=True` is interpreted as
            probabilities/weights for selecting a single door.  The length
            of the weights can be either a) the same as the number of doors
            or b) less than the number of doors.  In the latter case, the
            number of weights must align with the number of selectable
            doors per row, based on the `exclude_...` arguments below.
        weighted : bool, optional
            Treat the first argument as weights (see docs above).
            The default is False.
        exclude_current : bool, optional
            Don't allow re-revealing of doors that are already revealed. The default
            is True. This is a "redundant" action, which will throw an error
            if `allow_redundant=False` is specified.
        exclude_cars : bool, optional
            Don't allow doors containing cars to be revealed. The default is True.
            This is a spoiling action, which will throw an error if `allow_spoiled=False`
            is specified.
        exclude_picked : bool, optional
            Don't allow picked doors to be revealed. The default is True.
            This is a spoiling action, which will throw an error if
            `allow_spoiled=False` is specified.
        allow_spoiled : bool, optional
            Do not throw an error of the game is spoiled. The default is False.
            Spoiled games are recorded in the `spoiled` attribute of the
            simulation.
        allow_redundant : bool, optional
            Do not throw an error if currently revealed doors are selected.
            The default is True.

        Returns
        -------
        None.

        '''
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
    '''Class to model the host closing previously revealed doors.'''
    def __init__(self, doors=1, weighted=False, exclude_current=True,
                 allow_spoiled=False, allow_redundant=True):
        '''
        Class to model the host closing one or more revealed doors.

        Parameters
        ----------
        doors : int or list-like, optional
            Argument for specifying how many/which doors to close. The default is 1.
            Possible options are as follows:
            - a single integer is interpreted as the number of doors to
            select (randomly, with equal probability)
            - a list of integers with `weighted=False` is interpeted as
            specific doors to pick, e.g. `[0, 2]` selects the doors at
            index 0 and index 2.
            - a list of integers with `weighted=True` is interpreted as
            probabilities/weights for selecting a single door.  The length
            of the weights can be either a) the same as the number of doors
            or b) less than the number of doors.  In the latter case, the
            number of weights must align with the number of selectable
            doors per row, based on the `exclude_...` arguments below.
        weighted : bool, optional
            Treat the first argument as weights (see docs above).
            The default is False.
        exclude_current : bool, optional
            Don't allow closing of doors that are already closed. The default
            is True. This is a "redundant" action, which will throw an error
            if `allow_redundant=False` is specified.
        allow_spoiled : bool, optional
            Do not throw an error of the game is spoiled. The default is False.
            Spoiled games are recorded in the `spoiled` attribute of the
            simulation.
        allow_redundant : bool, optional
            Do not throw an error if currently closed doors are selected.
            The default is True.

        Returns
        -------
        None.

        '''
        super().__init__(target='revealed',
                         doors=doors,
                         weighted=weighted,
                         behavior='remove',
                         exclude_closed=exclude_current,
                         allow_redundant=allow_redundant,
                         allow_spoiled=allow_spoiled)
