from collections import namedtuple
from collections import OrderedDict
from datetime import datetime

from lib.constants import YNAB_COLUMNS


YNABRow = namedtuple('YNABRow', YNAB_COLUMNS)


class BankParserNotImplemented(Exception):
    pass


class CSVParser(object):

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
    def _parse_memo(transaction):
        name = transaction.get('merchantName') or \
               transaction.get('partnerName')
        memo_params = OrderedDict({
            'name': name,
            'city': transaction.get('merchantCity'),
            'reference': transaction.get('referenceText'),
        })
        memo = ''
        for key, value in memo_params.items():
            if value and value.strip():
                memo += '{}: {}, '.format(key, value)
        return memo.rstrip(', ')

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
            memo=self._parse_memo(transaction),
            outflow=self._parse_outflow(transaction),
            inflow=self._parse_inflow(transaction),
        ) for transaction in self._transactions]
