from dataclasses import dataclass
from datetime import datetime, time
from typing import List

import httpx
from devtools import debug

from graphql.loader import load_graphql

PHP_SESSION_ID = "3fcdae3a81974eaca3831c8942520a44"

URL_BASE = "https://tbn.devadministrateapp.com"
URL_GRAPHQL = "/graphql"
URL_RESOURCE_TYPES_SUBMIT = "/ResourceTypes/ajaxSubmitEditForm"


def unpack_json_response(r):
    data = r.json()["data"]
    assert len(data) == 1
    key = list(data)[0]
    edges = data[key]["edges"]
    return debug([edge['node'] for edge in edges])


@dataclass
class PlanCreateInput:
    name: str
    start: datetime
    end: datetime
    days: List[str]
    startTime: time
    endTime: time
    locationId: str


def create_plan(client, variables: PlanCreateInput):
    r = client.post(URL_GRAPHQL, json={
        'query': load_graphql("addPlan"),
        'variables':
            {'planInput':
                {
                    "name": variables.name,
                    "start": variables.start.isoformat(),
                    "end": variables.end.isoformat(),
                    "scheduleBounds": {
                        "days": variables.days,
                        "startTime": variables.startTime.isoformat(),
                        "endTime": variables.endTime.isoformat()
                    },
                    "locationId": variables.locationId
                }},
    })
    debug(r.status_code, r.reason_phrase, r.json())


def add_instructors_to_plan(client, plan_id: str, instructor_ids: List[str]):
    r = client.post(URL_GRAPHQL, json={
        'query': load_graphql("addInstructorsToPlan"),
        'variables': {'instInput': {
            'planId': plan_id,
            "contactIds": instructor_ids
        }}
    })
    debug(r.status_code, r.reason_phrase, r.json())


def read_plans(client):
    r = client.post(URL_GRAPHQL,
                    timeout=None,
                    json={'query': load_graphql("getAllPlans")})
    return unpack_json_response(r)


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


def read_course_templates(client):
    r = client.post(URL_GRAPHQL, json={'query': load_graphql("getAllCourseTemplates")})
    return unpack_json_response(r)


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


def main():
    with httpx.Client(base_url="https://tbn.devadministrateapp.com",
                      cookies={"PHPSESSID": PHP_SESSION_ID}) as client:
        # delete_resource_type(client, 12)
        # create_resource_type(client, "Climbing Rope", "For Climbing")
        # read_resource_types(client)
        # create_resource(client, "Smart Board", "UmVzb3VyY2VUeXBlOjM=")
        # read_resources(client)
        # read_resource_types(client)
        # read_course_templates(client)
        # read_instructors(client)

        # create_contact(client, "T3JnYW5pc2F0aW9uOjE=", "Wanda", "Montana")
        # read_contacts(client)

        # create_account(client, "Mo Bilhome")
        # read_accounts(client)

        # create_plan(client,
        #             PlanCreateInput(name="Modest Proposal: The Sequel",
        #                             start=datetime(year=2023, month=6, day=3, hour=9),
        #                             end=datetime(year=2023, month=6, day=7, hour=17),
        #                             days=["monday", "wednesday", "friday"],
        #                             startTime=time(hour=9),
        #                             endTime=time(hour=17),
        #                             locationId="TG9jYXRpb246Nzk="))
        # read_plans(client)

        add_instructors_to_plan(client, "UGxhbjo1", ["UGVyc29uOjQz", "UGVyc29uOjQy"])


main()
