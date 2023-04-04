from typing import Optional

from pydantic import BaseModel


class ResourceType(BaseModel):
    name: str


class Resource(BaseModel):
    id: str
    legacyId: int
    name: str
    type: Optional[ResourceType]
