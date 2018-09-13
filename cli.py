import click


from configurator import app_conf
from lib.constants import YNAB_COLUMNS
from lib.csv import CSVBuilder
from lib.ynab.parsers.csv import CSVParser


CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help']
)


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Interact with YNAB Importer"""


@cli.command()
def export_transactions():
    """ Generate YNAB ready CSV files for accounts defined in config.yml """

    for account in app_conf.accounts:
        print('Collecting data for account: {}'.format(account.name))

        transactions = account.connector.get_transactions()
        csv_rows = CSVParser(
            bank=account.bank,
            transactions=transactions,
        ).parse_rows()
        csv_builder = CSVBuilder(
            header=YNAB_COLUMNS,
            rows=csv_rows,
        )
        file_name = '{}.csv'.format(account.name)
        csv_builder.export_csv(file_name)


@cli.command()
def get_balances():
    """ Get balances for all accounts defined in config.yml """

    for account in app_conf.accounts:
        balance = account.connector.api.get_balance()['usableBalance']
        msg = 'Balance for account {} is {} EUR.'
        print(msg.format(account.name, balance))


if __name__ == '__main__':
    cli()
