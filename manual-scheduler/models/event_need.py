from typing import List, Optional

from pydantic import BaseModel

from graphql.loader import load_graphql
from data.api_client import ApiClient

from models.session_need import SessionNeed

client = ApiClient()


class CourseTemplate(BaseModel):
    title: str


class ScheduledEvent(BaseModel):
    code: str


class EventNeed(BaseModel):
    id: str
    legacyId: int
    courseTemplate: CourseTemplate
    sessionNeeds: List[SessionNeed]
    scheduledEvent: Optional[ScheduledEvent]


def read_course_templates(client):
    r = client.post("getAllCourseTemplates")
