from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(
        String(120), unique=False, nullable=False)
    last_name: Mapped[str] = mapped_column(
        String(120), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)

    # Relacion uno‑a‑muchos entre 'User' y 'Post'
    posts: Mapped[List["Post"]] = relationship(back_populates="user")

    followers: Mapped[List["Followers"]] = relationship(
        back_populates="followed",
        foreign_keys="Followers.followed_id")

    following: Mapped[List["Followers"]] = relationship(
        back_populates="follower",
        foreign_keys="Followers.follower_id")

    comments: Mapped[List["Comment"]] = relationship(back_populates="user")


def serialize(self):
    return {
        "id": self.id,
        "user_name": self.user_name,
        "email": self.email,
    }


class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # Columna de match con la tabla user
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    # Relacion entre 'User' y 'Post' del otro lado
    user: Mapped["User"] = relationship(back_populates="posts")
    media: Mapped[List["Media"]] = relationship(back_populates="post")

    comments: Mapped[List["Comment"]] = relationship(back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id
        }


class Media(db.Model):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    url: Mapped[str] = mapped_column(String(255), nullable=False)

    post: Mapped["Post"] = relationship(back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "url": self.url
        }


class Followers(db.Model):
    __tablename__ = "followers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    followed_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    follower: Mapped["User"] = relationship(
        foreign_keys=[follower_id],
        back_populates="following"
    )
    followed: Mapped["User"] = relationship(
        foreign_keys=[followed_id],
        back_populates="followers"
    )

    def serialize(self):
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "followed_id": self.followed_id
        }


class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    content: Mapped[str] = mapped_column(String(500), nullable=False)

    user: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "content": self.content
        }
