from pydantic import BaseModel


from pydantic import BaseModel, Field

class NoteCreate(BaseModel):
    title: str = Field(..., min_length=2)
    content: str = Field(..., min_length=2)


class NoteRead(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True


class ActionItemCreate(BaseModel):
    description: str = Field(..., min_length=2)


class ActionItemRead(BaseModel):
    id: int
    description: str
    completed: bool

    class Config:
        from_attributes = True
