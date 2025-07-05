from datetime import date

from pydantic import BaseModel, Field
from pydantic_extra_types.coordinate import Latitude, Longitude


class UserProfileCreateSchema(BaseModel):
    name: str
    gender: str
    date_of_birth: date = Field(..., representation="str")
    description: str | None
    latitude: Latitude
    longitude: Longitude

    class Config:
        from_attributes = True


class UserProfileUpdateSchema(BaseModel):
    description: str | None = None
    latitude: Latitude | None = None
    longitude: Longitude | None = None

    class Config:
        from_attributes = True
