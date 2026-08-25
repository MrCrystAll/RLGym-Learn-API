# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- A bunch of new endpoints under the prefix "/venv"
  - POST "/" allows you to create a virtual environment in the project's filesystem.
  - DELETE "/" allows you to delete (if exists) the virtual environment of the project.
  - GET "/" allows you to list all the packages of the project's virtual environment.
  - POST "/install" allows you to install a package to the virtual environment.
  - POST "/update" allows you to update a package of the virtual environment.
  - POST "/uninstall" allows you to uninstall a package from the virtual environment (If the package doesn't exist, the API will say that it has been successful uninstalling it).
  - POST "/install_requirements" allows you to pass a requirements file and install everything in it to the virtual environment.
  - GET "/package_update" allows you to fetch all the updatable packages.
- You can now specify an advanced configuration to the project creation, this will be used in the future for project settings.

## [0.1.6] - 2026-06-17

### Added

- A new field in the project metadata giving information on which version the project got created.
- A new migration guide is available

## [0.1.5] - 2026-06-02

### Added

- Added a "\_\_version\_\_" field to rlgym_learn_api, accessible via rlgym_learn_api.\_\_version\_\_

### Changed

- The new API schema for projects now differentiates return codes and return details based on the return code, for example
  - 200 returns the data the user asked for
  - 404 means the project or the root folder hasn't been found
  - 417 means the user / something else perturbated the creation of a project or the structure of the files
  - 422 is validation error, but this shouldn't occur unless manually making requests
- The new API schema for runs now differentiates return codes and return details based on the return code, for example
  - 200 returns the data the user asked for
  - 404 means the project/run is not found
  - 409 means the run already exists
  - 417 means the run config is invalid / doesn't exist
  - 422 is validation error, this can occur if the run schema is invalid. (Version difference)
- The new API schema for sessions now differentiates return codes and return details based on the return code, for example
  - 200 returns the data the user asked for
  - 404 means the run/session is not found
  - 417 means the run config is invalid / doesn't exist
  - 422 is validation error, this can occur if the run schema is invalid. (Version difference)

## [0.1.4] - 2026-05-28

### Changed

- The session start entrypoint now requires the port to send data back to the API.

## [0.1.3] - 2026-05-26

- First documented version
