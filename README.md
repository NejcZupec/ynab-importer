YNAB Importer
=============

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/93a6a2f00c314ada8f5c171f2d51b29a)](https://app.codacy.com/app/zupecnejc_3396/ynab-importer?utm_source=github.com&utm_medium=referral&utm_content=NejcZupec/ynab-importer&utm_campaign=badger)

Import transactions from [N26](https://n26.com) directly to [YNAB](https://www.youneedabudget.com/) via the API.


## Usage

Works with Python 3.7+.

Install requirements:

    pip install -r requirements.txt

Create `config.yml` file based on `config.yml.example` file.

Now you can run the following commands:

    python cli.py export_transactions

The command will export transactions to CSV files for all accounts listed in
`config.yml`. These files can be directly imported to YNAB via the UI.

    python cli.py get_balances

The command will return current balances for all accounts.

    python cli.py sync_transactions

The command will sync transactions for all accounts via YNAB API.


## Deploy to AWS Lambda

The application is managed with Serverless and is hosted on AWS Lambda.

### Prerequisites

1. Install [npm](https://www.npmjs.com/get-npm) 

1. Install Serverless globally: `npm install -g serverless`

1. Install dependencies: `npm install`

1. Setup [AWS Credentials](https://serverless.com/framework/docs/providers/aws/guide/credentials/)

### Deploy

Run `sls deploy -v`.


## CLI Installation and Autocomplete

First install ynab_importer package:

```sh
pip3 install .
```

#### Bash

Add the following lines to .bashrc:

```sh
# Enable autocomplete for ynab_importer's CLI
eval "$(_YNAB_IMPORTER_COMPLETE=source ynab_importer)"
```

#### Zsh

Add the following lines to .zshrc:

```sh
# Enable autocomplete for ynab_importer's CLI
autoload bashcompinit
bashcompinit
eval "$(_YNAB_IMPORTER_COMPLETE=source ynab_importer)"
```

## Python Requirements

This project uses [pip-compile-multi](https://github.com/peterdemin/pip-compile-multi)
project to manage Python requirements.

To add/change python requirements:

1. edit [requirements.in](requirements.in) file

1. run `pip-compile-multi -d .`
