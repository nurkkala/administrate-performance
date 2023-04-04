from pydantic import BaseModel


class PersonalName(BaseModel):
    firstName: str
    lastName: str


class Instructor(BaseModel):
    id: str
    legacyId: int
    personalName: PersonalName
