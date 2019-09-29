from lib import api as ynab_importer_api


def sync(event, context):
    ynab_importer_api.sync_transactions()

    return {
        "message": "Sync transactions executed!",
        "event": event
    }
