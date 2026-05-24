from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db, init_db
from models import Person
from schemas import PersonCreate, PersonUpdate, PersonOut

app = FastAPI(title="Memory API", version="0.1.0", root_path="/api")


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {"message": "Memory API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


# ===== ЛЮДИ =====

@app.get("/people", response_model=List[PersonOut])
def list_people(db: Session = Depends(get_db)):
    """Получить всех людей"""
    return db.query(Person).order_by(Person.created_at.desc()).all()


@app.get("/people/{person_id}", response_model=PersonOut)
def get_person(person_id: int, db: Session = Depends(get_db)):
    """Получить одного человека по id"""
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@app.post("/people", response_model=PersonOut, status_code=201)
def create_person(data: PersonCreate, db: Session = Depends(get_db)):
    """Создать нового человека"""
    person = Person(**data.model_dump())
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


@app.patch("/people/{person_id}", response_model=PersonOut)
def update_person(person_id: int, data: PersonUpdate, db: Session = Depends(get_db)):
    """Обновить человека"""
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(person, field, value)

    db.commit()
    db.refresh(person)
    return person


@app.delete("/people/{person_id}", status_code=204)
def delete_person(person_id: int, db: Session = Depends(get_db)):
    """Удалить человека"""
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    db.delete(person)
    db.commit()


# ===== СОБЫТИЯ =====

from models import Event
from schemas import EventCreate, EventUpdate, EventOut


@app.get("/events", response_model=List[EventOut])
def list_events(db: Session = Depends(get_db)):
    """Получить все события (новые сверху)"""
    return db.query(Event).order_by(Event.occurred_at.desc()).all()


@app.get("/events/{event_id}", response_model=EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """Получить одно событие"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@app.post("/events", response_model=EventOut, status_code=201)
def create_event(data: EventCreate, db: Session = Depends(get_db)):
    """Создать событие"""
    event_data = data.model_dump()
    # Если время не передано — ставим сейчас
    if event_data.get("occurred_at") is None:
        from datetime import datetime
        event_data["occurred_at"] = datetime.utcnow()
    event = Event(**event_data)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@app.patch("/events/{event_id}", response_model=EventOut)
def update_event(event_id: int, data: EventUpdate, db: Session = Depends(get_db)):
    """Обновить событие"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(event, field, value)

    db.commit()
    db.refresh(event)
    return event


@app.delete("/events/{event_id}", status_code=204)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    """Удалить событие"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(event)
    db.commit()


# ===== ИСТОРИИ =====

from models import Story
from schemas import StoryCreate, StoryUpdate, StoryOut


@app.get("/stories", response_model=List[StoryOut])
def list_stories(status: Optional[str] = None, db: Session = Depends(get_db)):
    """Получить истории. Можно фильтровать по status (active/completed)"""
    query = db.query(Story)
    if status:
        query = query.filter(Story.status == status)
    return query.order_by(Story.created_at.desc()).all()


@app.get("/stories/{story_id}", response_model=StoryOut)
def get_story(story_id: int, db: Session = Depends(get_db)):
    """Получить одну историю"""
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


@app.post("/stories", response_model=StoryOut, status_code=201)
def create_story(data: StoryCreate, db: Session = Depends(get_db)):
    """Создать историю"""
    story = Story(**data.model_dump())
    db.add(story)
    db.commit()
    db.refresh(story)
    return story


@app.patch("/stories/{story_id}", response_model=StoryOut)
def update_story(story_id: int, data: StoryUpdate, db: Session = Depends(get_db)):
    """Обновить историю"""
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(story, field, value)

    db.commit()
    db.refresh(story)
    return story


@app.delete("/stories/{story_id}", status_code=204)
def delete_story(story_id: int, db: Session = Depends(get_db)):
    """Удалить историю"""
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    db.delete(story)
    db.commit()
