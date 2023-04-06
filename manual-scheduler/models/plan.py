from dataclasses import dataclass
from datetime import time, datetime, timedelta
from typing import List, Optional, Self

from devtools import debug
from faker import Faker
from pydantic import BaseModel

from data.traverse import traverse
from graphql.loader import load_graphql
from data.api_client import URL_GRAPHQL
from models.event_need import EventNeed
from models.instructor import Contact
from models.location import Location
from models.resource import Resource

faker = Faker()


@dataclass
class PlanScheduleBoundsInput:
    startTime: time
    endTime: time
    days: List[str]


@dataclass
class PlanCreateInput:
    name: str
    start: datetime
    end: datetime
    scheduleBounds: PlanScheduleBoundsInput
    locationId: str


@dataclass
class PlanAddInstructorsInput:
    contactIds: List[str]
    planId: str


class ScheduleBounds(BaseModel):
    startTime: time
    endTime: time
    days: List[str]


class Status(BaseModel):
    solveStatus: str
    lifecycleState: str
    lastScore: Optional[str]
    explainScore: Optional[str]
    archivedAt: Optional[datetime]
    scheduledAt: Optional[datetime]


class Plan(BaseModel):
    id: str
    legacyId: int
    name: str
    start: datetime
    end: datetime
    scheduleBounds: ScheduleBounds
    status: Status
    location: Optional[Location]
    instructors: List[Contact]
    resources: List[Resource]
    eventNeeds: List[EventNeed]

    @classmethod
    def create_plan(cls, client, plan_create_input: PlanCreateInput) -> Self:
        r = client.post(URL_GRAPHQL, json={
            'query': load_graphql("addPlan"),
            'variables': {
                'planInput': {
                    "name": plan_create_input.name,
                    "start": plan_create_input.start.isoformat(),
                    "end": plan_create_input.end.isoformat(),
                    "scheduleBounds": {
                        "days": plan_create_input.scheduleBounds.days,
                        "startTime": plan_create_input.scheduleBounds.startTime.isoformat(),
                        "endTime": plan_create_input.scheduleBounds.endTime.isoformat()
                    },
                    "locationId": plan_create_input.locationId
                }},
        })
        content = traverse(r.json()["data"]["plan"]["create"]["plan"])
        return cls(**content)

    @staticmethod
    def add_instructors_to_plan(client, plan_add_instructors_input: PlanAddInstructorsInput):
        r = client.post(URL_GRAPHQL, json={
            'query': load_graphql("addInstructorsToPlan"),
            'variables': {'instInput': {
                'planId': plan_add_instructors_input.planId,
                "contactIds": plan_add_instructors_input.contactIds
            }}
        })
        return traverse(r.json()["data"]["plan"]["addInstructors"]["plan"])

    @classmethod
    def create_fake_plan(cls, client):
        start_date_time = faker.future_datetime()
        end_date_time = start_date_time + timedelta(days=7)
        location = Location.create_fake_location(client)

        plan_input = PlanCreateInput(
            name=faker.sentence(),
            start=start_date_time,
            end=end_date_time,
            scheduleBounds=PlanScheduleBoundsInput(
                startTime=time(hour=9),
                endTime=time(hour=17),
                days=["monday", "wednesday", "friday"]),
            locationId=location.id)
        plan = cls.create_plan(client, plan_input)

        contact = Contact.create_fake_contact(client, make_instructor=True)
        plan = plan.add_instructors_to_plan(
            client,
            PlanAddInstructorsInput(planId=plan.id,
                                    contactIds=[contact.id])
        )
        return plan

    @staticmethod
    def read_plans_list(client) -> List['Plan']:
        r = client.post(URL_GRAPHQL,
                        timeout=None,
                        json={
                            'query': load_graphql("getPlansList"),
                            "variables": {
                                "pageSize": 20,
                                "offset": 0,
                                "filters": [
                                    {
                                        "field": "isArchived",
                                        "operation": "eq",
                                        "value": "false"
                                    },
                                    {
                                        "field": "lifecycleState",
                                        "operation": "in",
                                        "values": [
                                            "DRAFT",
                                            "SOLVED",
                                            "SOLVING",
                                            "SOLVE_FAILED",
                                            "SCHEDULED"
                                        ]
                                    }
                                ]
                            }
                        })
        content = r.json()
        filtered_content = traverse(content["data"]["plans"])
        result = {
            "code": r.status_code,
            "reason": r.reason_phrase,
            "plans": [Plan(**ct) for ct in filtered_content],
        }
        return debug(result)
