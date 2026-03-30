from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Project
from ..schemas import ProjectCreate, ProjectRead

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=list[ProjectRead])
def list_projects(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = Query(50, le=200),
    sort: str = Query("-created_at"),
) -> list[ProjectRead]:
    stmt = select(Project)

    sort_field = sort.lstrip("-")
    order_fn = desc if sort.startswith("-") else asc
    if hasattr(Project, sort_field):
        stmt = stmt.order_by(order_fn(getattr(Project, sort_field)))
    else:
        stmt = stmt.order_by(desc(Project.created_at))

    rows = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
    return [ProjectRead.model_validate(row) for row in rows]


@router.post("/", response_model=ProjectRead, status_code=201)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)) -> ProjectRead:
    project = Project(name=payload.name, description=payload.description)
    db.add(project)
    db.flush()
    db.refresh(project)
    return ProjectRead.model_validate(project)


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db)) -> ProjectRead:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectRead.model_validate(project)


@router.patch("/{project_id}", response_model=ProjectRead)
def patch_project(project_id: int, payload: ProjectCreate, db: Session = Depends(get_db)) -> ProjectRead:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if payload.name is not None:
        project.name = payload.name
    if payload.description is not None:
        project.description = payload.description
    db.add(project)
    db.flush()
    db.refresh(project)
    return ProjectRead.model_validate(project)


@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db)) -> None:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
