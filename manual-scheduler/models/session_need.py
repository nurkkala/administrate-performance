from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from models.instructor import Contact
from models.resource import Resource


class Solution(BaseModel):
    start: datetime
    end: datetime
    instructors: List[Contact]
    resources: List[Resource]


class SessionNeed(BaseModel):
    id: str
    legacyId: int
    solution: Optional[Solution]
