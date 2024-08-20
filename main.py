from fastapi import FastAPI
from db.models import Base
from db.database import engine, create_database_if_not_exists
from routers import users, checked_sentence, keyboard, statics

app = FastAPI()


# Ensure the database is created on startup
@app.on_event("startup")
def on_startup():
    create_database_if_not_exists()
    Base.metadata.create_all(bind=engine)


print("start")

app.include_router(users.router)
app.include_router(checked_sentence.router)
app.include_router(keyboard.activation_router)
app.include_router(keyboard.keyboard_router)
app.include_router(statics.router)
