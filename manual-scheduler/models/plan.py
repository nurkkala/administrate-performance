from dataclasses import dataclass
from datetime import time, datetime, timedelta
from typing import List, Optional

from devtools import debug
from faker import Faker
from pydantic import BaseModel

from data.traverse import traverse
from graphql.loader import load_graphql
from data.api_client import URL_GRAPHQL
from models.event_need import EventNeed
from models.instructor import Instructor
from models.location import Location
from models.resource import Resource


class ScheduleBounds(BaseModel):
    startTime: time
    endTime: time
    days: List[str]


class Status(BaseModel):
    solveStatus: str
    lastScore: Optional[str]
    explainScore: Optional[str]
    archivedAt: Optional[datetime]
    scheduledAt: Optional[datetime]
    lifecycleState: str


class Plan(BaseModel):
    id: str
    legacyId: int
    name: str
    start: datetime
    end: datetime
    scheduleBounds: ScheduleBounds
    location: Optional[Location]
    status: Status
    instructors: List[Instructor]
    resources: List[Resource]
    eventNeeds: List[EventNeed]


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
                        "days": variables.scheduleBounds.days,
                        "startTime": variables.scheduleBounds.startTime.isoformat(),
                        "endTime": variables.scheduleBounds.endTime.isoformat()
                    },
                    "locationId": variables.locationId
                }},
    })
    content = r.json()["data"]["plan"]["create"]
    result = {
        "code": r.status_code,
        "reason": r.reason_phrase,
        "plan": Plan(**content["plan"]),
        "has_error": len(content["errors"]) > 0,
        "errors": content["errors"]
    }
    return debug(result)


def create_fake_plan(client):
    faker = Faker()

    start_date_time = faker.future_datetime()
    end_date_time = start_date_time + timedelta(days=7)

    plan = PlanCreateInput(
        name=faker.sentence(),
        start=start_date_time,
        end=end_date_time,
        scheduleBounds=PlanScheduleBoundsInput(
            startTime=time(hour=9),
            endTime=time(hour=17),
            days=["monday", "wednesday", "friday"])
    )

    create_plan(client, plan)


def read_plans_list(client):
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
                        }})

    content = r.json()
    filtered_content = traverse(content["data"]["plans"])
    result = {
        "code": r.status_code,
        "reason": r.reason_phrase,
        "plans": [Plan(**ct) for ct in filtered_content],
    }
    return debug(result)
