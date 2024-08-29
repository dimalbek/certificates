from fastapi import FastAPI
from auth import router as auth_router
from docs import router as files_router
from fastapi.staticfiles import StaticFiles
import models
from database import engine, Base


app = FastAPI()
Base.metadata.create_all(bind=engine)

# Mount the static files route
app.mount("/files", StaticFiles(directory="files"), name="files")

# Include the routers
app.include_router(auth_router, prefix="/auth")
app.include_router(files_router)

# # Start your FastAPI application
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)