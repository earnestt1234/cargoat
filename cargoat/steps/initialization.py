#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 12:17:34 2022

@author: earnestt1234
"""

import numpy as np

class InitDoorsEmpty:
    def __init__(self, doors):
        '''
        Initialize the simulation with a given number
        of doors.  All doors will contain goats.

        Parameters
        ----------
        doors : int
            Number of doors in simulation.

        Returns
        -------
        None.

        '''
        self.doors = doors

    def __call__(self, sim):
        shape = (sim.n, self.doors)
        sim.cars = np.zeros(shape, dtype=int)
        sim.picked = np.zeros(shape, dtype=int)
        sim.revealed = np.zeros(shape, dtype=int)
        sim.spoiled = np.zeros(sim.n, dtype=int)

class InitDoorsFixed:
    def __init__(self, placement=(1, 0, 0)):
        '''
        Initialize the simulation with a known, constant
        arrangement of cars and goats.

        Parameters
        ----------
        placement : list-like, optional
            Placement of cars & goats within each trial.
            Zeros signify goats while 1s signify cars.
            The default is (1, 0, 0), creating a three-door
            simulation, all with placement goat-goat-car.

        Returns
        -------
        None.

        '''
        self.placement = np.array(placement).astype(int)

    def __call__(self, sim):
        shape = (sim.n, len(self.placement))
        sim.cars = np.tile(self.placement, (sim.n, 1))
        sim.picked = np.zeros(shape, dtype=int)
        sim.revealed = np.zeros(shape, dtype=int)
        sim.spoiled = np.zeros(sim.n, dtype=int)

class InitDoorsRandom:
    def __init__(self, cars=1, goats=2):
        '''
        Initialize the doors with a given number of cars
        and goats - the placement itself is random.  This
        is closest to the original Monty Hall game.

        Parameters
        ----------
        cars : int, optional
            Number of cars per trial. The default is 1.
        goats : int, optional
            Number of goats per trial. The default is 2.

        Returns
        -------
        None.

        '''
        self.cars = cars
        self.goats = goats

    def __call__(self, sim):
        shape = (sim.n, self.cars + self.goats)
        sim.cars = np.zeros(shape, dtype=int)
        sim.picked = np.zeros(shape, dtype=int)
        sim.revealed = np.zeros(shape, dtype=int)
        sim.spoiled = np.zeros(sim.n, dtype=int)

        p = np.random.rand(shape[0], shape[1]).argsort(1)
        sim.cars[p < self.cars] = 1
