from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select

from database_model import engine, User, RedditAccount

from typing import Type

session = Session(engine)


def clear_db():
    for user in get_all_users():
        delete_user_by_login_name(str(user.login_name))


def check_user_exists(login_name: str) -> bool:
    return not (get_user_by_login_name(login_name=login_name) is None)


def check_reddit_account_exists(email: str) -> bool:
    return not (get_reddit_account_by_email(email=email) is None)


def check_user_password(login_name: str, password: str) -> bool:
    if not check_user_exists(login_name=login_name):
        return False
    return bool(get_user_by_login_name(login_name=login_name).user_password == password)


def check_reddit_password(email: str, password: str) -> bool:
    if not check_reddit_account_exists(email=email):
        return False
    return bool(get_reddit_account_by_email(email).password == password)


def get_user_by_login_name(login_name: str) -> User | None:
    return session.scalar(select(User).where(User.login_name == login_name))


def get_reddit_account_by_email(email: str) -> RedditAccount | None:
    return session.scalar(select(RedditAccount).where(RedditAccount.email == email))


def get_all_users() -> list[Type[User]]:
    return session.query(User).all()


def add_new_user(login_name: str, user_password: str) -> bool:
    if check_user_exists(login_name=login_name):
        return False

    session.add(User(login_name=login_name, user_password=user_password))
    session.commit()
    return True


def add_new_reddit_account(
    email: str,
    password: str,
    user_login_name: str,
    proxy: str,
    subscribe_start_date: datetime = None,
    subscribe_end_date: datetime = None
) -> bool:

    if not check_user_exists(login_name=user_login_name) or check_reddit_account_exists(email=email):
        return False

    user = get_user_by_login_name(login_name=user_login_name)
    session.add(RedditAccount(
        email=email,
        password=password,
        owner=user,
        proxy=proxy,
        subscribe_start_date=subscribe_start_date,
        subscribe_end_date=subscribe_end_date)
    )
    session.commit()
    return True


def delete_user_by_login_name(login_name: str) -> None:
    if check_user_exists(login_name=login_name):
        session.query(User).filter_by(login_name=login_name).delete()
        session.commit()


def delete_reddit_account_by_email(email: str) -> None:
    if check_reddit_account_exists(email=email):
        session.query(RedditAccount).filter_by(email=email).delete()
        session.commit()


def show_db(db_name) -> None:
    print(*session.query(db_name).all(), sep='\n')


if __name__ == "__main__":
    # add_new_user("someone", "123")
    add_new_reddit_account("other acc", "haha pas", "sasha", "1.1.1.1")
    show_db(RedditAccount)
