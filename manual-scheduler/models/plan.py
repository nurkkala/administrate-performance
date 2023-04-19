import random
from dataclasses import dataclass
from datetime import time, datetime, timedelta
from typing import List, Optional, Self

from devtools import debug
from faker import Faker
from pydantic import BaseModel

from data.api_client import ApiClient
from data.traverse import traverse
from models.event_need import EventNeed
from models.instructor import Contact
from models.location import Location
from models.resource import Resource

faker = Faker()
client = ApiClient()


@dataclass
class PlanScheduleBoundsInput:
    startTime: time
    endTime: time
    days: List[str]

    @classmethod
    def create_fake(cls):
        start_hour = random.randint(8, 11)
        end_hour = start_hour + random.randint(1, 6)
        return cls(
            startTime=time(hour=start_hour),
            endTime=time(hour=end_hour),
            days=random.sample(
                ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"],
                k=random.randint(1, 5)))


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


@dataclass
class PlanAddResourcesInput:
    resourceIds: List[str]
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
    def create_plan(cls, plan_create_input: PlanCreateInput) -> Self:
        r = client.post("addPlan",
                        variables={
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
                            }
                        })
        content = traverse(r.json()["data"]["plan"]["create"]["plan"])
        return cls(**content)

    @classmethod
    def add_instructors_to_plan(cls, plan_add_instructors_input: PlanAddInstructorsInput) -> Self:
        r = client.post("addInstructorsToPlan",
                        variables={
                            'instInput': {
                                'planId': plan_add_instructors_input.planId,
                                "contactIds": plan_add_instructors_input.contactIds
                            }
                        })
        content = traverse(r.json()["data"]["plan"]["addInstructors"]["plan"])
        return cls(**content)

    @staticmethod
    def add_resources_to_plan(plan_add_resources_input: PlanAddResourcesInput):
        r = client.post("addResourcesToPlan",
                        variables={
                            'resInput': {
                                'planId': plan_add_resources_input.planId,
                                'resourceIds': plan_add_resources_input.resourceIds
                            }
                        })
        return traverse(r.json()["data"]["plan"]["addResources"]["plan"])

    @classmethod
    def create_fake_plan(cls) -> Self:
        start_date_time = faker.future_datetime()
        end_date_time = start_date_time + timedelta(days=random.randint(3, 7))
        location = Location.create_fake_location()

        plan = cls.create_plan(PlanCreateInput(
            name=faker.sentence(),
            start=start_date_time,
            end=end_date_time,
            scheduleBounds=PlanScheduleBoundsInput.create_fake(),
            locationId=location.id))

        instructor = Contact.create_fake_contact(make_instructor=True)
        new_plan = Plan.add_instructors_to_plan(
            PlanAddInstructorsInput(planId=plan.id,
                                    contactIds=[instructor.id])
        )

        # `Plan` is now a `dict` instead of a `Plan`. :-(

        resources = [Resource.create_fake() for _ in range(5)]
        plan = Plan.add_resources_to_plan(
            PlanAddResourcesInput(planId=plan.id,
                                  resourceIds=[resource.id for resource in resources])
        )

        return plan

    @staticmethod
    def read_plans_list() -> List['Plan']:
        r = client.post("getPlansList",
                        variables={
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
                        })
        content = r.json()
        filtered_content = traverse(content["data"]["plans"])
        result = {
            "code": r.status_code,
            "reason": r.reason_phrase,
            "plans": [Plan(**ct) for ct in filtered_content],
        }
        return debug(result)
