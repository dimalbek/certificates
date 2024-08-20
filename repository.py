from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models import User
from serializers import UserCreate, UserLogin
from typing import List


class UsersRepository:
    def create_user(self, db: Session, user_data: UserCreate) -> User:
        try:
            # Check if the user already exists
            existing_user = db.query(User).filter(
                User.username == user_data.username).first()

            if existing_user:
                raise HTTPException(
                    status_code=400, detail="User already exists")

            new_user = User(
                username=user_data.username,
                password=user_data.password,
                name=user_data.name,
                surname=user_data.surname
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)

        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=400,
                                detail=f"Integrity error: {str(e)}")
        return new_user

    def get_user_by_username(self, db: Session, user_data: UserLogin) -> User:
        db_user = db.query(User).filter(
            User.username == user_data.username).first()
        if not db_user:
            raise HTTPException(status_code=404, detail=f"User with username {user_data.username} not found")
        return db_user

    def get_by_id(self, db: Session, user_id: int) -> User:
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user