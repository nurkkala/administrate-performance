from devtools import debug

PHP_SESSION_ID = "4c4edcfc5c334ae49c73ae67f7a2306a"
URL_BASE = "https://tbn.devadministrateapp.com"
URL_GRAPHQL = "/graphql"
BASE_URL = "https://tbn.devadministrateapp.com"


def unpack_json_response(r):
    data = r.json()["data"]
    assert len(data) == 1
    key = list(data)[0]
    edges = data[key]["edges"]
    return debug([edge['node'] for edge in edges])
