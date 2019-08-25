import logging


# this hack is needed to make AWS Lambda logs working
# https://stackoverflow.com/questions/1943747
root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    handlers=[
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger('YNAB Importer Logger')
