from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Note
from ..schemas import NoteCreate, NoteRead, NoteSearchResult

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=list[NoteRead])
def list_notes(db: Session = Depends(get_db)) -> list[NoteRead]:
    rows = db.execute(select(Note)).scalars().all()
    return [NoteRead.model_validate(row) for row in rows]


@router.post("/", response_model=NoteRead, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> NoteRead:
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.get("/search/", response_model=NoteSearchResult)
def search_notes(
    q: str | None = None,
    page: int = Query(1, ge=1, description="1-based page number"),
    page_size: int = Query(10, ge=1, le=100, description="Results per page"),
    sort: Literal["created_desc", "title_asc"] = Query(
        "created_desc", description="Sort order: created_desc or title_asc"
    ),
    db: Session = Depends(get_db),
) -> NoteSearchResult:
    stmt = select(Note)

    # Case-insensitive filter on title and content
    if q and q.strip():
        pattern = f"%{q.strip()}%"
        stmt = stmt.where(Note.title.ilike(pattern) | Note.content.ilike(pattern))

    # Total count before pagination
    total: int = db.execute(select(func.count()).select_from(stmt.subquery())).scalar_one()

    # Ordering
    if sort == "title_asc":
        stmt = stmt.order_by(Note.title.asc())
    else:  # created_desc: use id desc as creation-order proxy
        stmt = stmt.order_by(Note.id.desc())

    # Pagination
    stmt = stmt.offset((page - 1) * page_size).limit(page_size)

    rows = db.execute(stmt).scalars().all()
    return NoteSearchResult(
        items=[NoteRead.model_validate(row) for row in rows],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteRead.model_validate(note)
