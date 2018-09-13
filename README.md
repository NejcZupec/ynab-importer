YNAB Importer
=============

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/93a6a2f00c314ada8f5c171f2d51b29a)](https://app.codacy.com/app/zupecnejc_3396/ynab-importer?utm_source=github.com&utm_medium=referral&utm_content=NejcZupec/ynab-importer&utm_campaign=badger)

Import transactions from European banks directly to YNAB via the API.

To-do list:
- [ ] Integrate YNAB API
- [ ] Add support for other banks

**Currently works only export from n26 to a CSV file. The file is properly
formatted for YNAB import**


Supported Banks
---------------

- n26


Usage
-----

Works with Python >3.5.

Install requirements:

```sh
pip install -r requirements.txt
```

Create `config.yml` file based on `config.yml.example` file.

Run the following command:

```sh
python cli.py export_transactions
```

The command will export transactions to CSV files for all accounts listed in
`config.yml`. These files can be directly imported to YNAB via the UI.


CLI Installation and Autocomplete
---------------------------------

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
