from cli import sync_transactions


def sync(event, context):
    sync_transactions()

    return {
        "message": "Sync transactions executed!",
        "event": event
    }
