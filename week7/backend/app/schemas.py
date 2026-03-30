from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(None, min_length=1)


class ProjectRead(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    project_id: int | None = None


class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    project_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NotePatch(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    content: str | None = Field(None, min_length=1)
    project_id: int | None = None


class ActionItemCreate(BaseModel):
    description: str = Field(min_length=1)


class ActionItemRead(BaseModel):
    id: int
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ActionItemPatch(BaseModel):
    description: str | None = Field(None, min_length=1)
    completed: bool | None = None


