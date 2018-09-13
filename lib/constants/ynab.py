""" Here are listed all constants about YNAB service """

from collections import namedtuple


# columns used for importing transactions
YNAB_COLUMNS = ('date', 'payee', 'memo', 'outflow', 'inflow')

YNABRow = namedtuple('YNABRow', YNAB_COLUMNS)

YNABAccount = namedtuple('YNABAccount', (
    'name',  # string
    'connector',  # instance of Connector
    'ynab_account_id',  # string (UUID-like)
    'ynab_budget_id',  # string (UUID-like)
))
