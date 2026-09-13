from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    event,
    text,
)
from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String)
    bio: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[int] = mapped_column(
        Integer, server_default=text("(strftime('%s', 'now'))")
    )
    updated_at: Mapped[int] = mapped_column(
        Integer, server_default=text("(strftime('%s', 'now'))")
    )
    last_login: Mapped[int | None] = mapped_column(Integer)

    posts: Mapped[list["Post"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    excerpt: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        String, default="draft", server_default="draft", nullable=False
    )
    featured_image: Mapped[str | None] = mapped_column(String)
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[int] = mapped_column(
        Integer, server_default=text("(strftime('%s', 'now'))")
    )
    updated_at: Mapped[int] = mapped_column(
        Integer, server_default=text("(strftime('%s', 'now'))")
    )
    published_at: Mapped[int | None] = mapped_column(Integer)

    user: Mapped[User] = relationship(back_populates="posts")

    __table_args__ = (
        CheckConstraint(
            "status IN ('draft', 'published', 'archived')", name="ck_posts_status"
        ),
        Index("idx_posts_user_id", "user_id"),
        Index("idx_posts_status_published_at", "status", "published_at"),
    )
