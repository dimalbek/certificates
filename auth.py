from fastapi import APIRouter, Depends, Response, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from pydantic import EmailStr
from repository import UsersRepository
from serializers import UserCreate, UserLogin, UserInfo, DocumentInfo
from database import get_db

router = APIRouter()
users_repository = UsersRepository()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/users/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "Zakcination"
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt(user_id: int) -> str:
    body = {"user_id": user_id}
    token = jwt.encode(body, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_jwt(token: str) -> int:
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return data["user_id"]
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Could not validate credentials"
        )

@router.post("/users")
def post_signup(
    user_input: UserCreate,
    db: Session = Depends(get_db),
):
    user_input.password = hash_password(user_input.password)
    new_user = users_repository.create_user(db, user_input)
    return Response(
        status_code=200, content=f"Successful signup. User_id = {new_user.id}"
    )

@router.post("/users/login")
def post_login(
    username: EmailStr = Form(),
    password: str = Form(),
    db: Session = Depends(get_db),
):
    user_data = UserLogin(username=username, password=password)
    user = users_repository.get_user_by_username(db, user_data)
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_jwt(user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserInfo)
def get_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_id = decode_jwt(token)
    user = users_repository.get_by_id(db, user_id)
    
    # Create a list of DocumentInfo objects from user's documents
    documents = [
        DocumentInfo(
            id=document.id,
            filename=document.filename,
            uploaded_at=document.uploaded_at.strftime("%Y-%m-%d %H:%M:%S"),
            place=document.place
        ) for document in user.documents
    ]

    return UserInfo(
        id=user.id,
        username=user.username,
        name=user.name,
        surname=user.surname,
        documents=documents
    )


@router.get("/users/{user_id}", response_model=UserInfo)
def get_user_info(
    user_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        requesting_user_id = decode_jwt(token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    if requesting_user_id != 1:
        raise HTTPException(status_code=403, detail="Not enough permissions to view this information")

    user = users_repository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    documents = [
        DocumentInfo(
            id=document.id,
            filename=document.filename,
            uploaded_at=document.uploaded_at.strftime("%Y-%m-%d %H:%M:%S"),
            place=document.place
        ) for document in user.documents
    ]

    return UserInfo(
        id=user.id,
        username=user.username,
        name=user.name,
        surname=user.surname,
        documents=documents
    )