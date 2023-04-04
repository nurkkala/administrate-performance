from typing import Optional

from pydantic import BaseModel


class Country(BaseModel):
    code: str
    name: str


class Address(BaseModel):
    city: str
    country: Country


class Location(BaseModel):
    id: str
    legacyId: int
    name: str
    description: Optional[str]
    address: Optional[Address]
