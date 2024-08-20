from pydantic import BaseModel, EmailStr
from typing import List

class DocumentInfo(BaseModel):
    id: int
    filename: str
    uploaded_at: str
    place: str 
class UserCreate(BaseModel):
    username: EmailStr
    password: str
    name: str
    surname: str

class UserLogin(BaseModel):
    username: EmailStr
    password: str

class UserInfo(BaseModel):
    id: int
    username: EmailStr
    name: str
    surname: str
    documents: List[DocumentInfo]