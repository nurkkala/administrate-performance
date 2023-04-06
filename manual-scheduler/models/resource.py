from typing import Optional

from devtools import debug
from pydantic import BaseModel

from graphql.loader import load_graphql
from data.api_client import ApiClient

URL_RESOURCE_TYPES_SUBMIT = "/ResourceTypes/ajaxSubmitEditForm"

client = ApiClient()


class ResourceType(BaseModel):
    name: str


class Resource(BaseModel):
    id: str
    legacyId: int
    name: str
    type: Optional[ResourceType]


def create_resource(client, name, type_id):
    r = client.post("addResource",
                    variables={
                        "name": name,
                        "typeId": type_id
                    })
    debug(r.status_code, r.json())


def read_resources(client):
    r = client.post("getAllResources")


def create_resource_type(name, description):
    r = client.post_rest(url=URL_RESOURCE_TYPES_SUBMIT,
                         data={
                             "deleteResourceType": 0,
                             "id": 0,
                             "name": name,
                             "description": description
                         })
    debug(r.status_code, r.json())


def read_resource_types():
    r = client.post("getAllResourceTypes")


def delete_resource_type(legacy_id):
    r = client.post_rest(url=URL_RESOURCE_TYPES_SUBMIT,
                         data={
                             "deleteResourceType": 1,
                             "id": legacy_id,
                         })
    debug(r.status_code, r.json())
