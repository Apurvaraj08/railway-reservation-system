from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
import models

app = FastAPI()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Home API
@app.get("/")
def home():
    return {"message": "Railway API Running 🚀"}

# Add Passenger
@app.post("/passengers")
def add_passenger(name: str, age: int, gender: str, db: Session = Depends(get_db)):
    p = models.Passenger(name=name, age=age, gender=gender)
    db.add(p)
    db.commit()
    return {"message": "Passenger added"}

# View Trains
@app.get("/trains")
def get_trains(db: Session = Depends(get_db)):
    return db.query(models.Train).all()

def allocate_seat(train_id, db):
    seat = db.query(models.Seat).filter_by(
        train_id=train_id,
        is_available=True
    ).first()

    if not seat:
        return None

    seat.is_available = False
    db.commit()
    return seat

@app.post("/book")
def book_ticket(name: str, age: int, gender: str, train_id: int, db: Session = Depends(get_db)):

    # 1. Create passenger
    passenger = models.Passenger(name=name, age=age, gender=gender)
    db.add(passenger)
    db.commit()
    db.refresh(passenger)

    # 2. Allocate seat
    seat = allocate_seat(train_id, db)

    # 3. Decide status
    status = "CONFIRMED" if seat else "WAITING"

    # 4. Create booking
    booking = models.Booking(
        passenger_id=passenger.passenger_id,
        train_id=train_id,
        status=status
    )

    db.add(booking)
    db.commit()

    return {
        "message": "Booking created",
        "status": status
    }

# Create all database tables
Base.metadata.create_all(bind=engine)   