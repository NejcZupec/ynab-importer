import click
import yaml

from lib.banks.n26.connector import N26Connector
from lib.csv import CSVBuilder
from ynab import YNAB_COLUMNS


CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help']
)


class BankConnectorNotImplemented(BaseException):
    pass


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Interact with YNAB Importer"""


@cli.command()
def export_transactions():
    """ Generate YNAB ready CSV files for accounts defined in config.yml """

    cfg = yaml.safe_load(open('config.yml', 'r'))

    for account in cfg['accounts']:
        print('Collecting data for account: {}'.format(account['name']))

        if account['bank'] != 'n26':
            raise BankConnectorNotImplemented(account['bank'])

        connector = N26Connector(
            username=account['settings']['username'],
            password=account['settings']['password'],
            card_id=account['settings']['card_id'],
        )

        file_name = '{}.csv'.format(account['name'])
        csv_builder = CSVBuilder(
            header=YNAB_COLUMNS,
            rows=connector.get_ynab_rows(),
        )
        csv_builder.export_csv(file_name)


if __name__ == '__main__':
    cli()
