# Development Environment

## Getting Started

### Installation options
The list below shows a few different ways to get the development environment up and running.

- [Manual](../manual/README.md)
- [VSCode using devcontainers](../vscode/README.md)




## Run tests

Run unit- and integration tests.

### All tests

    $ pipenv run python -m pytest ../tests/

### Integration test:

    $ pipenv run unittest

### Unit test:

    $ pipenv run integrationtest

## Run linting:

Run PEP8 linting:

    $ pipenv run lint-flake8

## Uploading package manually

Steps to uploading package manually.
- Using pipenv first sync with development packages.
- Next build the tar.
- last upload it to pypi

Commands to run:

    pipenv sync -d 
    pipenv run build
    python run upload
