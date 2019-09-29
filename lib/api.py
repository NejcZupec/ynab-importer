import ynab

from configurator import app_conf
from lib.constants import YNAB_COLUMNS
from lib.csv import CSVBuilder
from lib.log import logger
from lib.pushed.api import PushedAPIClient
from lib.ynab.parsers.api import YNABAPIParser
from lib.ynab.parsers.csv import YNABCSVParser


def export_transactions():
    for account in app_conf.accounts:
        logger.info(f'Collecting data for account: {account.name}')

        transactions = account.connector.get_transactions()
        csv_rows = YNABCSVParser(
            bank=account.bank,
            transactions=transactions,
        ).parse_rows()
        csv_builder = CSVBuilder(
            header=YNAB_COLUMNS,
            rows=csv_rows,
        )
        file_name = f'{account.name}.csv'
        csv_builder.export_csv(file_name)


def get_balances():
    for account in app_conf.accounts:
        balance = account.connector.get_balance()
        logger.info(f'Balance for account {account.name} is {balance} EUR.')


def sync_transactions(import_sequence=1):
    for account in app_conf.accounts:
        logger.info(f'Syncing data for account: {account.name}')
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

        duplicates_count = len(response.data.bulk.duplicate_import_ids)
        new_transactions_count = len(response.data.bulk.transaction_ids)

        msg = f'Syncing {account.name} with YNAB - duplicates: {duplicates_count}, ' \
            f'new: {new_transactions_count}'
        logger.info(msg)

        if new_transactions_count > 0:
            PushedAPIClient.push(msg)
