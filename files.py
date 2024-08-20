import os
from fastapi import APIRouter, File, UploadFile, Depends, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import get_db
from models import Document
from auth import decode_jwt, oauth2_scheme
from jose import JWTError, jwt


router = APIRouter()

# Ensure the files directory exists
UPLOAD_DIR = "files/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/documents/")
async def upload_document(
    file: UploadFile = File(...),
    place: str = Form(None),  # Optional place field
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        user_id = decode_jwt(token)
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Could not validate credentials"
        )

    file_location = f"files/{file.filename}"
    
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())
    
    # Create a new document record in the database
    document = Document(
        user_id=user_id,
        filename=file.filename,
        content=file_location,
        place=place,  # Save the place field
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return {"filename": file.filename, "id": document.id}

@router.get("/download/{filename}")
async def download_document(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}