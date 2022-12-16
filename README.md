# cargoat
Cargoat is a package for creating custom [Monty Hall game](https://en.wikipedia.org/wiki/Monty_Hall_problem) simulations in Python.

![](https://raw.githubusercontent.com/earnestt1234/cargoat/main/img/goat_in_a_car.jpg)

Source: [Wikimedia](https://commons.wikimedia.org/wiki/File:Goat_in_a_car.jpg)

## About

I started working on cargoat after Monty-Hall-related-confusion induced by a recent statistics class.  My main goals were to create a simulation framework that:

- allows for arbitrary combination of actions by player & host.
- implements the repeated simulations and actions with numpy array operations, rather than for loops.

If you are (like me) curious about the Monty Hall problem and all its variations, hopefully you will enjoy tinkering with this library.  Though if you are new to learning about Python or Monty Hall, creating your own implementation will likely be far more valuable!

## Installation

cargoat will probably eventually be on PyPI; for now, it can be installed from GitHub using `pip`:

```
git clone https://github.com/earnestt1234/cargoat
cd cargoat
pip install .
```

## Quick Start

General steps for using cargoat:

1. Create a "game", AKA a list of actions to do.
2. Pick a number of times to simulate that game.
3. Run!

Here's what simulating the traditional Monty Hall problem looks like:

```python
import cargoat as cg

game = [cg.InitDoorsRandom(cars=1, goats=2),
        cg.Pick(),
        cg.Reveal(),
        cg.Switch(),
        cg.Finish()]

cg.play(game, n=1000)
```

Which will print out results which look like the following:

```
{'trials': 1000,
 'wins': 669,
 'losses': 331,
 'percent_wins': 66.9,
 'percent_losses': 33.1}
```

## Features

There are many [action types](https://earnestt1234.github.io/cargoat/cargoat/actions/index.html) which allow for simulation of all sorts of Monty Hall games:

- [Picking](https://earnestt1234.github.io/cargoat/cargoat/index.html#cargoat.Pick) & [revealing](https://earnestt1234.github.io/cargoat/cargoat/index.html#cargoat.Reveal) doors by methods - one or multiple at a time, and with optional probabilities.
- [Starting the game](https://earnestt1234.github.io/cargoat/cargoat/actions/initialization.html) with various arrangements of doors
- [Altering the number of doors](https://earnestt1234.github.io/cargoat/cargoat/actions/remodeling.html) mid game
- [Logical combination of actions](https://earnestt1234.github.io/cargoat/cargoat/actions/index.html#cargoat.actions.IfElse)
- [Applying any action with a certain probability](https://earnestt1234.github.io/cargoat/cargoat/actions/index.html#cargoat.actions.ChanceTo)

Additonally, cargoat allows you to have "spoiled" games where the actions of player or host violate the traditional rules.  The game results can be calculated with or without these spoiled games.

## Documentation

[API documentation is available here.](https://earnestt1234.github.io/cargoat/cargoat/) 

I am working on creating some vignettes showing more games, hopefully with some mathematical analysis, [a la this great post](https://www.untrammeledmind.com/2018/11/monty-hall-problem-and-variations-intuitive-solutions/).

## Contributing

Please raise any issues, suggestions, or requests on the [issues page](https://github.com/earnestt1234/cargoat/issues).  I would love to have other contribute - specific guidelines TBD.

The immediate goal for cargoat is to add a testing suite.

## License

[MIT](https://github.com/earnestt1234/cargoat/blob/main/LICENSE)

