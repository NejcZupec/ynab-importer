#!/usr/bin/env python

import click

from lib import api as ynab_importer_api


CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help']
)


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Interact with YNAB Importer"""


@cli.command()
def export_transactions():
    """ Generate YNAB ready CSV files for accounts defined in config.yml """
    ynab_importer_api.export_transactions()


@cli.command()
def get_balances():
    """ Get balances for all accounts defined in config.yml """
    ynab_importer_api.get_balances()


@cli.command()
@click.argument('import_sequence', required=False)
def sync_transactions(import_sequence=1):
    """ Sync transactions for all accounts with YNAB

    import_sequence - see https://support.youneedabudget.com/t/k95rt1
    """
    ynab_importer_api.sync_transactions(import_sequence)


if __name__ == '__main__':
    cli()
