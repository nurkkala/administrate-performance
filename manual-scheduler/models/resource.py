from typing import Optional

from devtools import debug
from pydantic import BaseModel

from graphql.loader import load_graphql
from data.api_client import URL_GRAPHQL, unpack_json_response

URL_RESOURCE_TYPES_SUBMIT = "/ResourceTypes/ajaxSubmitEditForm"


class ResourceType(BaseModel):
    name: str


class Resource(BaseModel):
    id: str
    legacyId: int
    name: str
    type: Optional[ResourceType]


def create_resource(client, name, type_id):
    r = client.post(URL_GRAPHQL, json={
        'query': load_graphql("addResource"),
        'variables': {
            "name": name,
            "typeId": type_id
        }})
    debug(r.status_code, r.json())


def read_resources(client):
    r = client.post(URL_GRAPHQL, json={'query': load_graphql("getAllResources")})
    return unpack_json_response(r)


def create_resource_type(client, name, description):
    r = client.post(URL_RESOURCE_TYPES_SUBMIT, data={
        "deleteResourceType": 0,
        "id": 0,
        "name": name,
        "description": description
    })
    debug(r.status_code, r.json())


def read_resource_types(client):
    r = client.post(URL_GRAPHQL, json={'query': load_graphql("getAllResourceTypes")})
    return unpack_json_response(r)


def delete_resource_type(client, legacy_id):
    r = client.post(URL_RESOURCE_TYPES_SUBMIT, data={
        "deleteResourceType": 1,
        "id": legacy_id,
    })
    debug(r.status_code, r.json())
