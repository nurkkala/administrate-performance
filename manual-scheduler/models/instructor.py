import random
from dataclasses import dataclass
from functools import cache
from typing import List, Self

from faker import Faker
from pydantic import BaseModel

from data.api_client import ApiClient
from data.traverse import traverse

faker = Faker()
client = ApiClient()


@dataclass
class AccountCreateInput:
    name: str

    @classmethod
    def create_fake(cls) -> Self:
        return AccountCreateInput(name=faker.word().upper())


class Account(BaseModel):
    id: str
    legacyId: int
    name: str
    isIndividual: bool

    @classmethod
    def create_account(cls, account_create_input: AccountCreateInput) -> Self:
        r = client.post("addAccount",
                        variables={
                            'accountInput': {
                                'name': account_create_input.name
                            }
                        })
        content = r.json()["data"]["account"]["create"]["account"]
        return cls(**content)

    @classmethod
    def create_fake_account(cls) -> Self:
        return cls.create_account(AccountCreateInput.create_fake())

    @staticmethod
    @cache
    def read_all_accounts() -> List['Account']:
        r = client.post("getAllAccounts")
        return [Account(**account) for account in traverse(r.json()["data"]["accounts"])]


@dataclass
class PersonalNameCreateInput:
    firstName: str
    lastName: str

    @classmethod
    def create_fake(cls):
        return PersonalNameCreateInput(
            firstName=faker.first_name(),
            lastName=faker.last_name())


@dataclass
class ContactCreateInput:
    accountId: str
    isInstructor: bool
    isStaff: bool
    isAdmin: bool
    personalName: PersonalNameCreateInput

    @classmethod
    def create_fake(cls, make_instructor=False) -> Self:
        accounts = Account.read_all_accounts()
        non_individual_accounts = [account for account in accounts if not account.isIndividual]
        assert len(non_individual_accounts) > 0

        is_instructor = True if make_instructor else faker.boolean()

        return ContactCreateInput(accountId=random.choice(non_individual_accounts).id,
                                  isInstructor=is_instructor,
                                  isStaff=faker.boolean(),
                                  isAdmin=faker.boolean(),
                                  personalName=PersonalNameCreateInput.create_fake())


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
    def create_contact(cls, contact_create_input: ContactCreateInput) -> Self:
        r = client.post("addContact",
                        variables={
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
                        })
        content = r.json()["data"]["contact"]["create"]["contact"]
        return cls(**content)

    @classmethod
    def create_fake_contact(cls, make_instructor=False) -> Self:
        accounts = Account.read_all_accounts()
        non_individual_accounts = [account for account in accounts if not account.isIndividual]
        assert len(non_individual_accounts) > 0
        return cls.create_contact(ContactCreateInput.create_fake(make_instructor))

    @staticmethod
    def read_contacts() -> List['Contact']:
        r = client.post("getAllContacts")
        return [Contact(**contact) for contact in traverse(r.json()["data"]["contacts"])]

