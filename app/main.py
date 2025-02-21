from fastapi import FastAPI
from app.routers import books, auth
from app.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(books.router, prefix="/api", tags=["Books"])
