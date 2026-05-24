from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


# Таблицы связей многие-ко-многим

event_people = Table(
    "event_people",
    Base.metadata,
    Column("event_id", ForeignKey("events.id"), primary_key=True),
    Column("person_id", ForeignKey("people.id"), primary_key=True),
)

event_stories = Table(
    "event_stories",
    Base.metadata,
    Column("event_id", ForeignKey("events.id"), primary_key=True),
    Column("story_id", ForeignKey("stories.id"), primary_key=True),
)

story_people = Table(
    "story_people",
    Base.metadata,
    Column("story_id", ForeignKey("stories.id"), primary_key=True),
    Column("person_id", ForeignKey("people.id"), primary_key=True),
)


# Основные модели

class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    category = Column(String(50), default="friends")
    context = Column(Text, default="")
    avatar_url = Column(String(500), default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    notes = relationship("Note", back_populates="person", cascade="all, delete-orphan")
    events = relationship("Event", secondary=event_people, back_populates="people")
    stories = relationship("Story", secondary=story_people, back_populates="people")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    title = Column(String(300), nullable=False)
    description = Column(Text, default="")
    event_type = Column(String(50), default="meeting")
    location = Column(String(300), default="")
    occurred_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    people = relationship("Person", secondary=event_people, back_populates="events")
    stories = relationship("Story", secondary=event_stories, back_populates="events")


class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True)
    title = Column(String(300), nullable=False)
    description = Column(Text, default="")
    icon = Column(String(50), default="book")
    color = Column(String(20), default="blue")
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

    events = relationship("Event", secondary=event_stories, back_populates="stories")
    people = relationship("Person", secondary=story_people, back_populates="stories")


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("people.id"), nullable=False)
    content = Column(Text, nullable=False)
    voice_url = Column(String(500), default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    person = relationship("Person", back_populates="notes")
