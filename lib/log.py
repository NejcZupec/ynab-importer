import logging


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    handlers=[
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger('YNAB Importer Logger')
