#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 08:52:01 2022

@author: earnestt1234
"""

from cargoat.steps.generic import GenericAction

class Pick(GenericAction):
    '''Class modeling the contestant picking a door.'''
    def __init__(self, doors=1, weighted=False, exclude_current=True,
                 exclude_revealed=True, add=False, allow_spoiled=False,
                 allow_redundant=True):
        '''
        Class to model the contestant picking one or more doors.
        Picks are significant for determining the winners of games -
        trials where doors containing cars are picked are considered wins.

        Parameters
        ----------
        doors : int or list-like, optional
            Argument for specifying how many/which doors to pick. The default is 1.
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
            Don't allow re-selection of doors that are already picked. The default
            is True. This is a "redundant" action, which will throw an error
            if `allow_redundant=False` is specified.
        exclude_revealed : bool, optional
            Don't allow revealed/open doors to be picked. The default is True.
            This is a spoiling action, which will throw an error if `allow_spoiled=False`
            is specified.
        add : bool, optional
            Add picks generated by this action to existing picks.
            The default is False, in which case the old picks are replaced
            by the current action.
        allow_spoiled : bool, optional
            Do not throw an error of the game is spoiled. The default is False.
            Spoiled games are recorded in the `spoiled` attribute of the
            simulation.
        allow_redundant : bool, optional
            Do not throw an error if currently picked doors are repicked.
            The default is True.

        Returns
        -------
        None.

        '''
        behavior = 'add' if add else 'overwrite'
        super().__init__(target='picked',
                         doors=doors,
                         weighted=weighted,
                         behavior=behavior,
                         exclude_picked=exclude_current,
                         exclude_revealed=exclude_revealed,
                         allow_redundant=allow_redundant,
                         allow_spoiled=allow_spoiled)

class Unpick(GenericAction):
    '''Class modeling the contestant deselecting a door.'''

    def __init__(self, doors=1, weighted=False, exclude_current=True,
                 allow_spoiled=False, allow_redundant=True):
        '''
        Class to model the contestant deselecting ("unpicking") one or more
        doors.

        Note that this action does not need to be explicitly called switching
        picks from one door to another, for example when switching doors in the
        traditional Monty Hall game.  Rather, it is for removing a previously
        picked door without assiging a new pick.

        Parameters
        ----------
        doors : int or list-like, optional
            Argument for specifying how many/which doors to unpick. The default is 1.
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
            Don't allow unpicking of doors that aren't picked. The default is True.
            This is a "redundant" action, which will throw an error
            if `allow_redundant=False` is specified.
        allow_spoiled : bool, optional
            Do not throw an error of the game is spoiled. The default is False.
            Spoiled games are recorded in the `spoiled` attribute of the
            simulation.
        allow_redundant : bool, optional
            Do not throw an error if currently unpicked doors are unpicked.
            The default is True.

        Returns
        -------
        None.

        '''
        super().__init__(target='picked',
                         doors=doors,
                         weighted=weighted,
                         behavior='remove',
                         exclude_unpicked=exclude_current,
                         allow_redundant=allow_redundant,
                         allow_spoiled=allow_spoiled)
