import click
import ynab


from configurator import app_conf
from lib.constants import YNAB_COLUMNS
from lib.csv import CSVBuilder
from lib.pushed.api import PushedAPIClient
from lib.ynab.parsers.api import YNABAPIParser
from lib.ynab.parsers.csv import YNABCSVParser


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
        csv_rows = YNABCSVParser(
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
        balance = account.connector.get_balance()
        msg = 'Balance for account {} is {} EUR.'
        print(msg.format(account.name, balance))


@cli.command()
@click.argument('import_sequence', required=False)
def sync_transactions(import_sequence=1):
    """ Sync transactions for all accounts with YNAB

    import_sequence - see https://support.youneedabudget.com/t/k95rt1
    """

    for account in app_conf.accounts:
        print('Syncing data for account: {}'.format(account.name))
        account_id = account.ynab_account_id
        budget_id = account.ynab_budget_id

        transactions = account.connector.get_transactions()

        api_transactions = YNABAPIParser(
            bank=account.bank,
            transactions=transactions,
        ).parse(account_id, import_sequence)

        response = ynab.TransactionsApi().bulk_create_transactions(
            budget_id=budget_id,
            transactions=api_transactions,
        )

        duplicates = response.data.bulk.duplicate_import_ids
        new_transactions = response.data.bulk.transaction_ids

        msg = 'Successfully synced account {} with YNAB: duplicates: {},' \
              ' new: {}'.format(
                account.name, len(duplicates), len(new_transactions))

        PushedAPIClient.push(msg)


if __name__ == '__main__':
    cli()
