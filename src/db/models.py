"""
SQLAlchemy models — matches the table design in DESIGN.md.
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


def gen_uuid():
    return str(uuid.uuid4())


class Image(Base):
    __tablename__ = "images"

    id = Column(String, primary_key=True, default=gen_uuid)
    file_path = Column(String, nullable=False)
    subject = Column(String)
    category = Column(String, index=True)
    attributes = Column(JSON, default=list)
    caption = Column(Text)
    confidence = Column(Float)
    flagged = Column(Boolean, default=False)
    cost_usd = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    vector = relationship("ImageVector", back_populates="image", uselist=False)


class ImageVector(Base):
    __tablename__ = "image_vectors"

    image_id = Column(String, ForeignKey("images.id"), primary_key=True, index=True)
    embedding = Column(JSON)  # stored as a list of floats

    image = relationship("Image", back_populates="vector")


class Post(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True, default=gen_uuid)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    expected_category = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    vector = relationship("PostVector", back_populates="post", uselist=False)


class PostVector(Base):
    __tablename__ = "post_vectors"

    post_id = Column(String, ForeignKey("posts.id"), primary_key=True, index=True)
    embedding = Column(JSON)
    cost_usd = Column(Float, default=0.0)

    post = relationship("Post", back_populates="vector")


class Suggestion(Base):
    __tablename__ = "suggestions"

    id = Column(String, primary_key=True, default=gen_uuid)
    post_id = Column(String, ForeignKey("posts.id"), index=True)
    image_id = Column(String, ForeignKey("images.id"), nullable=True)
    similarity_score = Column(Float, nullable=True)
    guard_result = Column(String)  # "accepted" / "rejected" / "no_match"
    guard_reason = Column(Text, nullable=True)
    review_status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)