count_query = {
    "query": {"bool": {"must": [{"term": {"is_deleted": False}}]}},
}
search_param = {
    "query": {"bool": {"must": [{"term": {"is_deleted": False}}]}},
    "fields": ["name"],
    "_source": False,
}
