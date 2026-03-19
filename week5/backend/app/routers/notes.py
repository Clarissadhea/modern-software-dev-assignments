from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem, Note
from ..schemas import ExtractionResult, NoteCreate, NoteListResponse, NoteRead
from ..services.extract import extract_all

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=NoteListResponse)
def list_notes(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> NoteListResponse:
    total = db.execute(select(func.count()).select_from(Note)).scalar_one()
    offset = (page - 1) * page_size
    rows = db.execute(select(Note).offset(offset).limit(page_size)).scalars().all()
    return NoteListResponse(items=[NoteRead.model_validate(r) for r in rows], total=total)


@router.post("/", response_model=NoteRead, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> NoteRead:
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.get("/search/", response_model=list[NoteRead])
def search_notes(q: str | None = None, db: Session = Depends(get_db)) -> list[NoteRead]:
    if not q:
        rows = db.execute(select(Note)).scalars().all()
    else:
        rows = (
            db.execute(select(Note).where((Note.title.contains(q)) | (Note.content.contains(q))))
            .scalars()
            .all()
        )
    return [NoteRead.model_validate(row) for row in rows]


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteRead.model_validate(note)


@router.post("/{note_id}/extract", response_model=ExtractionResult)
def extract_note(
    note_id: int,
    apply: bool = False,
    db: Session = Depends(get_db),
) -> ExtractionResult:
    """Extract #hashtags and - [ ] action items from a note's content.

    Pass ``apply=true`` to persist the extracted action items to the database.
    """
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    result = extract_all(note.content)

    if apply:
        for task_text in result["action_items"]:
            db.add(ActionItem(description=task_text, completed=False))
        db.flush()

    return ExtractionResult(tags=result["tags"], action_items=result["action_items"])
