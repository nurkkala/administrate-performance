from typing import Optional, Dict

import httpx

from graphql.loader import load_graphql

PHP_SESSION_ID = "4c4edcfc5c334ae49c73ae67f7a2306a"
URL_BASE = "https://tbn.devadministrateapp.com"
URL_GRAPHQL = "/graphql"
BASE_URL = "https://tbn.devadministrateapp.com"


class ApiClient:
    """
    The API client. Implemented as a singleton.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.httpx = httpx.Client(base_url=BASE_URL,
                                               cookies={"PHPSESSID": PHP_SESSION_ID})
        return cls._instance

    def __del__(self):
        self._instance.httpx.close()

    def post(self,
             graphql_file_name: str,
             variables: Optional[Dict] = None,
             url=URL_GRAPHQL):
        """Post a GraphQL operation."""
        json = {
            'query': load_graphql(graphql_file_name)
        }
        if variables is not None:
            json['variables'] = variables

        return self._instance.httpx.post(url, timeout=None, json=json)

    def post_form(self, url: str, data: Dict):
        """Post an HTTP form."""
        return self._instance.httpx.post(url, timeout=None, data=data)

# Credits
# - https://python-patterns.guide/gang-of-four/singleton/
