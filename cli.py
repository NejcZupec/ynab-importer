#!/usr/bin/env python

import click

from lib import api as ynab_importer_api


CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help']
)


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Interact with YNAB Importer"""


@cli.command("e")
def export_transactions():
    """ Export transactions to CSV """
    ynab_importer_api.export_transactions()


@cli.command("b")
def get_balances():
    """ Get balances """
    ynab_importer_api.get_balances()


@cli.command("s")
@click.argument('import_sequence', required=False)
def sync_transactions(import_sequence=1):
    """ Sync transactions for all accounts

    import_sequence - see https://support.youneedabudget.com/t/k95rt1
    """
    ynab_importer_api.sync_transactions(import_sequence)


if __name__ == '__main__':
    cli()
