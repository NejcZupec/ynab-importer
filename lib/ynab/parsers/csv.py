from collections import namedtuple
from datetime import datetime

from lib.constants import YNAB_COLUMNS
from lib.ynab.parsers.common import n26_memo_parser


YNABRow = namedtuple('YNABRow', YNAB_COLUMNS)


class BankParserNotImplemented(Exception):
    pass


class YNABCSVParser(object):

    def __init__(self, bank, transactions):
        self._bank = bank
        self._transactions = transactions

    def parse_rows(self):
        if self._bank != 'n26':
            raise BankParserNotImplemented(self._bank)
        return N26TransactionsParser(self._transactions).parse_rows()


class TransactionsParser(object):

    def parse_rows(self):
        raise NotImplementedError


class N26TransactionsParser(TransactionsParser):
    """ Convert N26 transactions to YNAB CSV rows """

    def __init__(self, n26_transactions):
        self._transactions = n26_transactions

    @staticmethod
    def _parse_date(transaction):
        created = transaction.get('visibleTS')
        if not created:
            return None
        return datetime.fromtimestamp(created/1000).strftime('%d/%m/%Y')

    @staticmethod
    def _parse_outflow(transaction):
        amount = float(transaction.get('amount'))
        if amount < 0.0:
            return amount * (-1)
        return None

    @staticmethod
    def _parse_inflow(transaction):
        amount = float(transaction.get('amount'))
        if amount > 0.0:
            return amount
        return None

    def parse_rows(self):
        return [YNABRow(
            date=self._parse_date(transaction),
            payee=None,
            memo=n26_memo_parser(transaction),
            outflow=self._parse_outflow(transaction),
            inflow=self._parse_inflow(transaction),
        ) for transaction in self._transactions]
