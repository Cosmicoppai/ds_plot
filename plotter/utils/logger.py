import logging

logging.basicConfig(filename='apache_parsing.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

LOGGER = logging.getLogger(__name__)
