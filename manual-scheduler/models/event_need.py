from typing import List, Optional

from pydantic import BaseModel

from models.session_need import SessionNeed


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
