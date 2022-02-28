# Installation and running locally (for development)

The following sections describes how to install and run the project locally for development and debugging.

## Requirements
This project requires the following requirements:
- Python 3.8+
- Pipenv


## First time installation
Make sure to upgrade your system packages for good measure:

    $ pip install --upgrade --user setuptools pip

Install Pipenv:

    $ pip install --upgrade --user pipenv

Then install project dependencies (including dev-packages):

    $ pipenv update --dev

Define necessary options (described in a section above):

    SQL_URI=<SQL connection string>
    OIDC_CLIENT_ID=<OpenID Connect Client ID>
    OIDC_CLIENT_SECRET=<OpenID Connect Client secret>
    OIDC_AUTHORITY_URL=<OpenID Connect authority URL>

Navigate to the source directory:

    $ cd src/

Apply database migrations:

    $ pipenv run alembic --config=migrations/alembic.ini upgrade head