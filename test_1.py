import uvicorn # opens a port so computer can listen for web traffic
from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, create_engine
# create_engine manages connection to database file
from sqlalchemy.orm import declarative_base
#create python classes that are mapped to database tables
from sqlalchemy.orm import sessionmaker
#bypasses the need for credentials when connecting to database
import os
from dotenv import load_dotenv

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
engine=create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()
# sessionmaker:class factory, returns a class when instantiated creates a new Session
# autocommit: if False, transactions are not automatically committed after each statement
#autoflush:If fa;se gives manual control over when changes are sent to database
#bind=engine:connects session factory to db engine

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)


Base.metadata.create_all(bind=engine)

app= FastAPI()


@app.get("/items/")
async def list_items():
    db=SessionLocal()
    items=db.query(Item).all()
    return items

@app.post("/items/")#creates item endpoint
async def create_item(name:str,description:str):
    db=SessionLocal()
    db_item=Item(name=name,description=description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    db=SessionLocal()
    item=db.query(Item).filter(Item.id==item_id).first()
    return item

@app.put("/items/{item_id}")
async def update_item(item_id: int, name: str, description: str):
    db = SessionLocal()
    db_item = db.query(Item).filter(Item.id == item_id).first()
    db_item.name = name
    db_item.description = description
    db.commit()
    return db_item
    
@app.delete("/items/{item_id}")
async def delete_item(item_id:int):
    db=SessionLocal()
    db_item=db.query(Item).filter(Item.id == item_id).first()
    db.delete(db_item)
    db.commit()
    return { "message":"Item deleted succesfully"}

if __name__=="__main__":
    uvicorn.run(app)