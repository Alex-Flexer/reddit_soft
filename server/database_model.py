from typing import Optional, List
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import create_engine, ForeignKey

engine = create_engine("sqlite:///database_users.db")


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    login_name: Mapped[Optional[str]]

    user_password: Mapped[Optional[str]]

    reddit_accounts: Mapped[List["RedditAccount"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return f"{self.id} {self.login_name} {self.user_password}"

    def __repr__(self) -> str:
        return f"{self.id} {self.login_name} {self.user_password}"


class RedditAccount(Base):
    __tablename__ = "reddit_account_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    owner: Mapped["User"] = relationship(back_populates="reddit_accounts")

    owner_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))

    email: Mapped[Optional[str]]

    password: Mapped[Optional[str]]

    subscribe_start_date: Mapped[Optional[datetime]]

    subscribe_end_date: Mapped[Optional[datetime]]

    proxy: Mapped[str]

    def __str__(self) -> str:
        return f"{self.id} {self.email} {self.password} {self.owner.login_name}"

    def __repr__(self) -> str:
        return f"{self.id} {self.email} {self.password} {self.owner.login_name}"


Base.metadata.create_all(engine)
