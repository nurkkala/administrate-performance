import random
from dataclasses import dataclass
from functools import cache
from typing import List, Self

from devtools import debug
from faker import Faker
from pydantic import BaseModel

from data.traverse import traverse
from graphql.loader import load_graphql
from data.api_client import URL_GRAPHQL, unpack_json_response

faker = Faker()


@dataclass
class AccountCreateInput:
    name: str


class Account(BaseModel):
    id: str
    legacyId: int
    name: str
    isIndividual: bool

    @classmethod
    def create_account(cls, client, account_create_input: AccountCreateInput) -> Self:
        r = client.post(URL_GRAPHQL,
                        json={
                            'query': load_graphql("addAccount"),
                            'variables': {
                                'accountInput': {
                                    'name': account_create_input.name
                                }
                            }
                        })
        content = r.json()["data"]["account"]["create"]["account"]
        return cls(**content)

    @classmethod
    def create_fake_account(cls, client) -> Self:
        return cls.create_account(client, AccountCreateInput(name=faker.word().upper()))

    @staticmethod
    @cache
    def read_all_accounts(client) -> List['Account']:
        r = client.post(URL_GRAPHQL, json={'query': load_graphql("getAllAccounts")})
        return [Account(**account) for account in traverse(r.json()["data"]["accounts"])]


@dataclass
class PersonalNameCreateInput:
    firstName: str
    lastName: str


@dataclass
class ContactCreateInput:
    accountId: str
    isInstructor: bool
    isStaff: bool
    isAdmin: bool
    personalName: PersonalNameCreateInput


class PersonalName(BaseModel):
    firstName: str
    lastName: str


class Contact(BaseModel):
    id: str
    legacyId: int
    isInstructor: bool
    isStaff: bool
    isAdmin: bool
    personalName: PersonalName
    account: Account

    @classmethod
    def create_contact(cls, client, contact_create_input: ContactCreateInput) -> Self:
        r = client.post(URL_GRAPHQL,
                        json={
                            'query': load_graphql("addContact"),
                            'variables': {
                                'contactInput': {
                                    'accountId': contact_create_input.accountId,
                                    'isInstructor': contact_create_input.isInstructor,
                                    'isStaff': contact_create_input.isStaff,
                                    'isAdmin': contact_create_input.isAdmin,
                                    'personalName': {
                                        'firstName': contact_create_input.personalName.firstName,
                                        'lastName': contact_create_input.personalName.lastName
                                    }
                                }
                            }
                        })
        content = r.json()["data"]["contact"]["create"]["contact"]
        return cls(**content)

    @classmethod
    def create_fake_contact(cls, client) -> Self:
        accounts = Account.read_all_accounts(client)
        non_individual_accounts = [account for account in accounts if not account.isIndividual]
        assert len(non_individual_accounts) > 0
        return cls.create_contact(client,
                                  ContactCreateInput(accountId=random.choice(non_individual_accounts).id,
                                                     isInstructor=faker.boolean(),
                                                     isStaff=faker.boolean(),
                                                     isAdmin=faker.boolean(),
                                                     personalName=PersonalNameCreateInput(
                                                         firstName=faker.first_name(),
                                                         lastName=faker.last_name()
                                                     )))

    @staticmethod
    def read_contacts(client) -> List['Contact']:
        r = client.post(URL_GRAPHQL, json={'query': load_graphql("getAllContacts")})
        return [Contact(**contact) for contact in traverse(r.json()["data"]["contacts"])]


class Instructor(BaseModel):
    id: str
    legacyId: int
    isInstructor: bool
    isStaff: bool
    isAdmin: bool
    personalName: PersonalName


def add_instructors_to_plan(client, plan_id: str, instructor_ids: List[str]):
    r = client.post(URL_GRAPHQL, json={
        'query': load_graphql("addInstructorsToPlan"),
        'variables': {'instInput': {
            'planId': plan_id,
            "contactIds": instructor_ids
        }}
    })
    debug(r.status_code, r.reason_phrase, r.json())


def read_instructors(client):
    r = client.post(URL_GRAPHQL, json={'query': load_graphql("getAllInstructors")})
    return unpack_json_response(r)
