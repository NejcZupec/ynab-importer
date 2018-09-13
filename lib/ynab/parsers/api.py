from datetime import datetime

from ynab import SaveTransaction
from ynab import TransactionsWrapper

from lib.ynab.parsers.common import n26_memo_parser


class BankParserNotImplemented(Exception):
    pass


class YNABAPIParser(object):

    def __init__(self, bank, transactions):
        self._bank = bank
        self._transactions = transactions

    def parse(self, account_id, import_sequence):
        if self._bank != 'n26':
            raise BankParserNotImplemented(self._bank)
        return N26TransactionsAPIParser(self._transactions).parse(
            account_id, import_sequence)


class N26TransactionsAPIParser(object):
    """ Convert N26 transactions to YNAB API transactions """

    def __init__(self, transactions):
        self._transactions = transactions

    @staticmethod
    def _parse_date(transaction):
        created = transaction.get('visibleTS')
        if not created:
            return None
        return datetime.fromtimestamp(created / 1000).strftime('%Y-%m-%d')

    @staticmethod
    def _parse_amount(transaction):
        return int(float(transaction.get('amount')) * 1000)

    @classmethod
    def _parse_import_id(cls, transaction, import_sequence):
        """ More info: https://support.youneedabudget.com/t/k95rt1 """
        return 'YNAB:{amount}:{date}:{sequence}'.format(
            amount=cls._parse_amount(transaction),
            date=cls._parse_date(transaction),
            sequence=import_sequence,
        )

    def parse(self, account_id, import_sequence=1):
        """ Prepare transactions data for API """
        return TransactionsWrapper([SaveTransaction(
            date=self._parse_date(transaction),
            amount=self._parse_amount(transaction),
            memo=n26_memo_parser(transaction),
            account_id=account_id,
            import_id=self._parse_import_id(transaction, import_sequence),
        ) for transaction in self._transactions])