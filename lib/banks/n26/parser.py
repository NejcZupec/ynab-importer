from collections import OrderedDict
from datetime import datetime

from ynab import YNABRow


class TransactionsParser(object):
    """ Convert N26 transactions to YNAB rows """

    def __init__(self, _transactions):
        self._transactions = _transactions

    @staticmethod
    def _parse_date(transaction):
        created = transaction.get('createdTS')
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
