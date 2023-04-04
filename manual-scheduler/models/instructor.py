from typing import List

from devtools import debug
from pydantic import BaseModel

from graphql.loader import load_graphql
from data.api_client import URL_GRAPHQL, unpack_json_response


class PersonalName(BaseModel):
    firstName: str
    lastName: str


class Instructor(BaseModel):
    id: str
    legacyId: int
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


def create_contact(client, account_id, first_name, last_name):
    r = client.post(URL_GRAPHQL, json={
        'query': load_graphql("addContact"),
        'variables': {'contactInput': {
            "accountId": account_id,
            "personalName": {
                "firstName": first_name,
                "lastName": last_name
            }
        }},
    })
    debug(r.status_code, r.reason_phrase, r.json())


def read_contacts(client):
    r = client.post(URL_GRAPHQL, json={'query': load_graphql("getAllContacts")})
    return unpack_json_response(r)


def create_account(client, name):
    r = client.post(URL_GRAPHQL, json={
        'query': load_graphql("addAccount"),
        'variables': {'accountInput': {
            'name': name
        }}
    })
    debug(r.status_code, r.reason_phrase, r.json())


def read_accounts(client):
    r = client.post(URL_GRAPHQL, json={'query': load_graphql("getAllAccounts")})
    return unpack_json_response(r)


def read_instructors(client):
    r = client.post(URL_GRAPHQL, json={'query': load_graphql("getAllInstructors")})
    return unpack_json_response(r)
