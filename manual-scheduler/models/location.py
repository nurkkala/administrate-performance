import random
from dataclasses import dataclass
from functools import cache
from typing import Optional, List, Self

from faker import Faker
from pydantic import BaseModel

from data.api_client import ApiClient
from data.traverse import traverse

faker = Faker()
api_client = ApiClient()


class Company(BaseModel):
    id: str
    legacyId: Optional[int]
    code: str
    name: str

    @staticmethod
    def read_all_companies() -> List['Company']:
        r = api_client.post("getAllCompanies")
        return [Company(**company) for company in traverse(r.json()["data"]["companies"])]


class Province(BaseModel):
    code: str
    name: str


class Country(BaseModel):
    id: str
    code: str
    name: str
    provinces: Optional[List[Province]]
    timeZones: Optional[List[str]]

    @staticmethod
    @cache
    def read_all_countries(client) -> List['Country']:
        r = client.post("getAllCountries")
        return [Country(**country) for country in r.json()["data"]["countries"]]

    @classmethod
    def read_random_country(cls, client) -> Self:
        countries = cls.read_all_countries(client)
        assert len(countries) > 0
        return random.choice(countries)


@dataclass
class RegionCreateInput:
    code: str
    name: str
    companyId: str


class Region(BaseModel):
    id: str
    # legacyId: int - Duplicates `code` for some reason.
    code: str
    name: str
    company: Company
    countries: List[Country]

    @classmethod
    def create_region(cls, region_create_input: RegionCreateInput):
        r = api_client.post("addRegion",
                            variables={"regInput":
                                {
                                    'code': region_create_input.code,
                                    'name': region_create_input.name,
                                    'companyId': region_create_input.companyId
                                }
                            })
        result = r.json()["data"]["regions"]["create"]["region"]
        return cls(**result)

    @classmethod
    def fake_region(cls):
        companies = Company.read_all_companies()
        assert len(companies) > 0
        return cls.create_region(
            RegionCreateInput(code=faker.word().upper(),
                              name=" ".join(faker.words()).title(),
                              companyId=companies[0].id))

    @staticmethod
    def read_all_regions() -> List['Region']:
        r = api_client.post("getAllRegions")
        return [Region(**region) for region in traverse(r.json()["data"]["regions"])]


class Address(BaseModel):
    city: str
    country: Country


@dataclass
class LocationCreateInput:
    name: str
    description: str
    regionId: str

    @classmethod
    def create_fake(cls):
        regions = Region.read_all_regions()
        assert len(regions) > 0
        return cls(name=faker.word().upper(),
                   description=faker.sentence(),
                   regionId=random.choice(regions).id)


class Location(BaseModel):
    id: str
    legacyId: int
    name: str
    description: Optional[str]
    address: Optional[Address]
    region: Optional[Region]

    @classmethod
    def create_location(cls, location_create_input: LocationCreateInput) -> Self:
        r = api_client.post("addLocation",
                            variables={
                                "locInput": {
                                    'name': location_create_input.name,
                                    'description': location_create_input.description,
                                    'regionId': location_create_input.regionId
                                }
                            })
        result = r.json()["data"]["location"]["create"]["location"]
        return cls(**result)

    @classmethod
    def create_fake_location(cls) -> Self:
        return cls.create_location(LocationCreateInput.create_fake())
