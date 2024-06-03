from elasticsearch import Elasticsearch
from config.index import (
    ELASTIC_SEARCH_URL,
    ELASTIC_SEARCH_PASSWORD,
    ELASTIC_SEARCH_USERNAME,
)

# from config.index import ES_URL, ES_NAME, ES_PASSWORD

es = Elasticsearch(
    ELASTIC_SEARCH_URL,
    basic_auth=(ELASTIC_SEARCH_USERNAME, ELASTIC_SEARCH_PASSWORD),
    timeout=30,
    max_retries=10,
    retry_on_timeout=True,
)
