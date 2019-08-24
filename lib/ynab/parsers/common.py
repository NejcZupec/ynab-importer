from collections import OrderedDict


def n26_memo_parser(transaction):
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
