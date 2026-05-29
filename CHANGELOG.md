# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- The new API schema for projects now differentiates return codes and return details based on the return code, for example
  - 200 returns the data the user asked for
  - 404 means the project or the root folder hasn't been found
  - 417 means the user / something else perturbated the creation of a project or the structure of the files
  - 422 is validation error, but this shouldn't occur unless manually making requests

## [0.1.4] - 2026-05-28

### Changed

- The session start entrypoint now requires the port to send data back to the API.

## [0.1.3] - 2026-05-26

- First documented version
