#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 22:10:52 2022

@author: earnestt1234
"""

from cargoat.actions.generic import GenericAction

class PlaceCar(GenericAction):
    def __init__(self, doors=1, weighted=False, exclude_current=True,
                 exclude_revealed=True, allow_spoiled=False,
                 allow_redundant=True):
        '''
        Class to model the host adding additional cars to one or more
        doors.  Cars are significant for determining wins and losses:
        trials where doors containing cars are also selected are
        considered wins.

        Parameters
        ----------
        doors : int or list-like, optional
            Argument for specifying how many/which doors to place cars behind.
            The default is 1. Possible options are as follows:

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
            Don't allow placing cars in doors already containing cars. The default
            is True. This is a "redundant" action, which will throw an error
            if `allow_redundant=False` is specified.
        exclude_revealed : bool, optional
            Don't allow cars to be placed in revealed doors. The default is True.
            This action does not spoil the game.
        allow_spoiled : bool, optional
            Do not throw an error of the game is spoiled. The default is False.
            Spoiled games are recorded in the `spoiled` attribute of the
            simulation.
        allow_redundant : bool, optional
            Do not throw an error if doors already containing cars are selected.
            The default is True.

        Returns
        -------
        None.

        '''
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
        '''
        Class to model the host removing cars placed behind one or more
        doors.

        Parameters
        ----------
        doors : int or list-like, optional
            Argument for specifying how many/which doors to place cars behind.
            The default is 1. Possible options are as follows:

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
            Don't allow removing cars in doors already containing goats. The default
            is True. This is a "redundant" action, which will throw an error
            if `allow_redundant=False` is specified.
        exclude_revealed : bool, optional
            Don't allow cars to be removed from revealed doors. The default is True.
            This action does not spoil the game, though revealed cars
            should only occur in spoiled gmes.
        allow_spoiled : bool, optional
            Do not throw an error of the game is spoiled. The default is False.
            Spoiled games are recorded in the `spoiled` attribute of the
            simulation.
        allow_redundant : bool, optional
            Do not throw an error if doors already containing goats are selected.
            The default is True.

        Returns
        -------
        None.

        '''
        super().__init__(target='revealed',
                         doors=doors,
                         weighted=weighted,
                         behavior='remove',
                         exclude_carless=exclude_current,
                         allow_redundant=allow_redundant,
                         allow_spoiled=allow_spoiled)
