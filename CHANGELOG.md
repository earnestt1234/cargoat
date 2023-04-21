# Changelog for cargoat

##  [0.1.0](https://github.com/earnestt1234/cargoat/releases/tag/0.1.0) - 4/20/2023

### Added

- Test suite
- `__eq__()` method for simulations
- Warning for simulations constructed with non-binary integers in `MontyHallSim.from_arrays()`
- Simulation property for determining if simulation is empty
- Simulation method for initializing unpopulated doors (`MontyHallSim.init_doors()`)
- Simulation method for reverting to empty state (`MontyHallSim.make_emtpy()`)
- Better parsing of arguments for `MontyHallSim.select()`

### Fixed

- Make `cargoat.RemoveDoors()` work with integer input
- Some typos in documentation

### Changed

- `cargoat.combine_sims()` can now accept empty simulations
- Make actions return the sim in `__call__()` method
- Rename `cargoat.actions.results.Finish()` to `cargoat.actions.results.ShowResults()`

## [0.0.1](https://github.com/earnestt1234/cargoat/releases/tag/0.0.1) - 12/18/2022

First tagged release.