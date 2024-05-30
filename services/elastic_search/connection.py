from elasticsearch import Elasticsearch

# from config.index import ES_URL, ES_NAME, ES_PASSWORD

ES_URL = "https://electric-es-staging.es.eastus2.azure.elastic-cloud.com:9243/"
ES_NAME = "elastic"
ES_PASSWORD = "3rbC8UePJgRWxs2VtzDeFuSb"

es = Elasticsearch(
    ES_URL,
    basic_auth=(ES_NAME, ES_PASSWORD),
    timeout=30,
    max_retries=10,
    retry_on_timeout=True,
)
