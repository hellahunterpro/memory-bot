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


# ===== ЗАМЕТКИ =====

from models import Note
from schemas import NoteCreate, NoteOut


@app.get("/people/{person_id}/notes", response_model=List[NoteOut])
def list_person_notes(person_id: int, db: Session = Depends(get_db)):
    """Получить все заметки про человека (новые сверху)"""
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    return db.query(Note).filter(Note.person_id == person_id).order_by(Note.created_at.desc()).all()


@app.post("/people/{person_id}/notes", response_model=NoteOut, status_code=201)
def create_note(person_id: int, data: NoteCreate, db: Session = Depends(get_db)):
    """Добавить заметку про человека"""
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    note = Note(person_id=person_id, **data.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """Удалить заметку"""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(note)
    db.commit()


# ===== СВЯЗИ: ЛЮДИ ↔ СОБЫТИЯ =====

@app.post("/events/{event_id}/people/{person_id}", status_code=204)
def add_person_to_event(event_id: int, person_id: int, db: Session = Depends(get_db)):
    """Добавить человека к событию"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    if person not in event.people:
        event.people.append(person)
        db.commit()


@app.delete("/events/{event_id}/people/{person_id}", status_code=204)
def remove_person_from_event(event_id: int, person_id: int, db: Session = Depends(get_db)):
    """Убрать человека из события"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    if person in event.people:
        event.people.remove(person)
        db.commit()


@app.get("/events/{event_id}/people", response_model=List[PersonOut])
def list_event_people(event_id: int, db: Session = Depends(get_db)):
    """Список людей участвовавших в событии"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event.people


# ===== СВЯЗИ: СОБЫТИЯ ↔ ИСТОРИИ =====

@app.post("/stories/{story_id}/events/{event_id}", status_code=204)
def add_event_to_story(story_id: int, event_id: int, db: Session = Depends(get_db)):
    """Добавить событие к истории"""
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event not in story.events:
        story.events.append(event)
        db.commit()


@app.delete("/stories/{story_id}/events/{event_id}", status_code=204)
def remove_event_from_story(story_id: int, event_id: int, db: Session = Depends(get_db)):
    """Убрать событие из истории"""
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event in story.events:
        story.events.remove(event)
        db.commit()


@app.get("/stories/{story_id}/events", response_model=List[EventOut])
def list_story_events(story_id: int, db: Session = Depends(get_db)):
    """Хронология событий истории (новые сверху)"""
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return sorted(story.events, key=lambda e: e.occurred_at, reverse=True)


# ===== СВЯЗИ: ЛЮДИ ↔ ИСТОРИИ =====

@app.post("/stories/{story_id}/people/{person_id}", status_code=204)
def add_person_to_story(story_id: int, person_id: int, db: Session = Depends(get_db)):
    """Добавить человека к истории"""
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    if person not in story.people:
        story.people.append(person)
        db.commit()


@app.delete("/stories/{story_id}/people/{person_id}", status_code=204)
def remove_person_from_story(story_id: int, person_id: int, db: Session = Depends(get_db)):
    """Убрать человека из истории"""
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    if person in story.people:
        story.people.remove(person)
        db.commit()


@app.get("/stories/{story_id}/people", response_model=List[PersonOut])
def list_story_people(story_id: int, db: Session = Depends(get_db)):
    """Список людей участвующих в истории"""
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story.people


# ===== ПОИСК =====

from pydantic import BaseModel


class SearchResult(BaseModel):
    """Универсальный результат поиска"""
    type: str  # "person" / "event" / "story" / "note"
    id: int
    title: str  # имя/название
    snippet: str  # фрагмент с совпадением
    context: dict  # дополнительная инфа (например person_id для notes)


@app.get("/search", response_model=List[SearchResult])
def search(q: str, db: Session = Depends(get_db)):
    """
    Поиск по всем сущностям. Минимум 2 символа.
    """
    if len(q.strip()) < 2:
        raise HTTPException(status_code=400, detail="Query must be at least 2 characters")
    
    pattern = f"%{q}%"
    results = []
    
    # Поиск по людям (имя, контекст)
    people = db.query(Person).filter(
        (Person.name.ilike(pattern)) | (Person.context.ilike(pattern))
    ).all()
    for p in people:
        snippet = p.context if q.lower() in (p.context or "").lower() else p.name
        results.append(SearchResult(
            type="person",
            id=p.id,
            title=p.name,
            snippet=snippet[:200],
            context={"category": p.category}
        ))
    
    # Поиск по событиям (название, описание, место)
    events = db.query(Event).filter(
        (Event.title.ilike(pattern)) | 
        (Event.description.ilike(pattern)) | 
        (Event.location.ilike(pattern))
    ).all()
    for e in events:
        snippet = e.description if q.lower() in (e.description or "").lower() else e.title
        results.append(SearchResult(
            type="event",
            id=e.id,
            title=e.title,
            snippet=snippet[:200],
            context={"event_type": e.event_type, "occurred_at": e.occurred_at.isoformat()}
        ))
    
    # Поиск по историям (название, описание)
    stories = db.query(Story).filter(
        (Story.title.ilike(pattern)) | (Story.description.ilike(pattern))
    ).all()
    for s in stories:
        snippet = s.description if q.lower() in (s.description or "").lower() else s.title
        results.append(SearchResult(
            type="story",
            id=s.id,
            title=s.title,
            snippet=snippet[:200],
            context={"status": s.status, "icon": s.icon}
        ))
    
    # Поиск по заметкам (содержимое)
    notes = db.query(Note).filter(Note.content.ilike(pattern)).all()
    for n in notes:
        # Для заметок нужно подтянуть имя человека к которому она относится
        person = db.query(Person).filter(Person.id == n.person_id).first()
        person_name = person.name if person else "Неизвестно"
        results.append(SearchResult(
            type="note",
            id=n.id,
            title=f"Заметка про {person_name}",
            snippet=n.content[:200],
            context={"person_id": n.person_id, "person_name": person_name}
        ))
    
    return results
