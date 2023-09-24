from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import schema, operation as op
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=op.User)
def create_user(user: op.UserCreate, db: Session = Depends(get_db)):
    db_user = op.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return op.create_user(db=db, user=user)


@app.get("/users/", response_model=List[op.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = op.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=op.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = op.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=op.Item)
def create_item_for_user(
    user_id: int, item: op.ItemCreate, db: Session = Depends(get_db)
):
    return op.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[op.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = op.get_items(db, skip=skip, limit=limit)
    return items


