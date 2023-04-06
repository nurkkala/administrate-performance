import random
from typing import Optional, Self, List

from devtools import debug
from faker import Faker
from pydantic import BaseModel

from data.api_client import ApiClient
from data.traverse import traverse

URL_RESOURCE_TYPES_SUBMIT = "/ResourceTypes/ajaxSubmitEditForm"

faker = Faker()
client = ApiClient()


class ResourceType(BaseModel):
    id: str
    legacyId: int
    name: str
    description: str

    @classmethod
    def create_resource_type(cls, name: str, description: str) -> Self:
        # There is _no_ GraphQL op to create a resource type. Submit a form instead.
        r = client.post_form(url=URL_RESOURCE_TYPES_SUBMIT,
                             data={
                                 "deleteResourceType": 0,
                                 "id": 0,
                                 "name": name,
                                 "description": description
                             })
        assert r.json()["success"]
        # There _is_ an op to read resource type(s).
        return cls.read_one_resource_type(name)

    @classmethod
    def create_fake(cls) -> Self:
        return cls.create_resource_type(
            name=faker.word(),
            description=faker.sentence()
        )

    @staticmethod
    def read_one_resource_type(name: str) -> 'Self':
        r = client.post("getOneResourceType",
                        variables={
                            'name': name
                        })
        result = traverse(r.json()["data"]["resourceTypes"])
        assert len(result) == 1
        return ResourceType(**result[0])

    @staticmethod
    def read_all_resource_types() -> List['Self']:
        r = client.post("getAllResourceTypes")
        return [ResourceType(**rt) for rt in traverse(r.json()["data"]["resourceTypes"])]

    @staticmethod
    def delete_resource_type(legacy_id: int):
        r = client.post_form(url=URL_RESOURCE_TYPES_SUBMIT,
                             data={
                                 "deleteResourceType": 1,
                                 "id": legacy_id,
                             })
        debug(r.status_code, r.json())


class Resource(BaseModel):
    id: str
    legacyId: int
    name: str
    type: Optional[ResourceType]

    @classmethod
    def create_resource(cls, name: str, type_id: str) -> Self:
        r = client.post("addResource",
                        variables={
                            "name": name,
                            "typeId": type_id
                        })
        result = r.json()["data"]["resources"]["create"]
        return Resource(**result)

    @classmethod
    def create_fake(cls) -> Self:
        resource_types = ResourceType.read_all_resource_types()
        assert len(resource_types) > 0
        return cls.create_resource(name=faker.word(),
                                   type_id=random.choice(resource_types).id)

    @staticmethod
    def read_all_resources() -> List['Self']:
        r = client.post("getAllResources")
        return [Resource(**r) for r in traverse(r.json()["data"]["resourceTypes"])]
