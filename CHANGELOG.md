# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2019-08-12
### Fixed
- Channel init_consumer_if_necessary iterable type

## [1.1.0] - 2019-08-11
### Added
- Channel global tests

### Changed
- Migrate Consumer start, run and stop methods to async

### Fixed
- Consumer attributes queue and filter_size to public
- Channel start and stop methods
- Channels methods Cython compliance

## [1.0.12] - 2019-08-09
### Changed
- PyDoc fixes

## [1.0.11] - 2019-08-09
### Added
- Channel new consumer methods

## [1.0.10] - 2019-08-08
### Added
- Channel internal_producer

## [1.0.9] - 2019-08-07
### Changed
- Channel creation utility refactored in two different methods

## [1.0.8] - 2019-08-06
### Added
- Channel creation utility

## [1.0.7] - 2019-08-04
### Added
- Channel 'modify' method that calls all producers modify method
- Channel 'register_producer' method to register all its producers.

## [1.0.6] - 2019-08-03
### Added
- constants.py file

### Modified 
- Import way with __init__.py files

### Removed
- Unused evaluator package

## [1.0.5] - 2019-08-03
### Added
- Producer 'modify' method

## [1.0.4] - 2019-06-10
### Fixed
- ExchangeChannel deprecated imports

## [1.0.3] - 2019-06-10
### Removed
- [OctoBot-Trading] migrate exchange channels to OctoBot-Trading

## [1.0.2] - 2019-06-09
### Fixed
- [OctoBot-Trading] Exchange get_name() method deprecated

## [1.0.1] - 2019-05-27
### Changed
- Migrate to cython with pure python
