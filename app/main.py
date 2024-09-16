from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from app.models import Item as DBItem  # SQLAlchemy model for database
from app.schemas import ItemCreate, ItemRead  # Pydantic models for API
from app.database import get_db
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/admin/items/", response_model=list[ItemRead])
def admin_items(request: Request, db: Session = Depends(get_db)):
    items = db.query(DBItem).all()
    return templates.TemplateResponse("admin_items.html", {"request": request, "items": items})

@app.get("/admin/items/{item_id}", response_model=ItemRead)
def admin_item(request: Request, item_id: int, db: Session = Depends(get_db)):
    item = db.query(DBItem).filter(DBItem.id == item_id).first()
    return templates.TemplateResponse("admin_item.html", {"request": request, "item": item})



@app.post("/admin/items/", response_model=ItemRead)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = DBItem(name=item.name, price=item.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
