from datetime import time, datetime
from typing import List, Optional

from pydantic import BaseModel

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
