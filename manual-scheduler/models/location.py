from dataclasses import dataclass
from typing import Optional, List

from devtools import debug
from pydantic import BaseModel

from data.api_client import URL_GRAPHQL, unpack_json_response
from data.traverse import traverse
from graphql.loader import load_graphql


@dataclass
class RegionCreateInput:
    code: str
    name: str
    companyId: str


@dataclass
class LocationCreateInput:
    name: str
    regionId: str


class Company(BaseModel):
    id: str
    legacyId: int
    code: str
    name: str


class Province(BaseModel):
    code: str
    name: str


class Country(BaseModel):
    id: str
    code: str
    name: str
    provinces: List[Province]
    timeZones: List[str]


class Region(BaseModel):
    id: str
    legacyId: int
    name: str
    code: str
    countries: List[Country]


class Address(BaseModel):
    city: str
    country: Country


class Location(BaseModel):
    id: str
    legacyId: int
    name: str
    description: Optional[str]
    address: Optional[Address]


def create_region(client, region_create_input: RegionCreateInput):
    r = client.post(URL_GRAPHQL, json={
        'query': load_graphql("addRegion"),
        'variables': {

        }
    })


def read_countries(client):
    r = client.post(URL_GRAPHQL, json={'query': load_graphql("getAllCountries")})
    return [Country(**country) for country in r.json()["data"]["countries"]]


def read_companies(client):
    r = client.post(URL_GRAPHQL, json={'query': load_graphql("getAllCompanies")})
    return [Company(**company) for company in traverse(r.json()["data"]["companies"])]
