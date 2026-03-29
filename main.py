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
def book_ticket(name: str, age: int, gender: str, train_id: int, seat_type: str = "", berth_type: str = "", db: Session = Depends(get_db)):

    # 1. Create passenger
    passenger = models.Passenger(name=name, age=age, gender=gender)
    db.add(passenger)
    db.commit()
    db.refresh(passenger)

    # 2. Allocate seat based on preferences
    seat = allocate_seat(train_id, db)

    # 3. Decide status
    status = "CONFIRMED" if seat else "WAITING"

    # 4. Store seat preferences
    seat_pref = f"{seat_type}-{berth_type}" if seat_type and berth_type else "Any"

    # 5. Create booking
    booking = models.Booking(
        passenger_id=passenger.passenger_id,
        train_id=train_id,
        status=status,
        seat_preference=seat_pref
    )

    db.add(booking)
    db.commit()

    return {
        "message": "Booking created",
        "status": status,
        "seat_id": seat.seat_id if seat else "N/A",
        "booking_id": booking.booking_id
    }

# Cancel Booking
@app.delete("/cancel/{booking_id}")
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    try:
        booking = db.query(models.Booking).filter_by(booking_id=booking_id).first()
        
        if not booking:
            return {"message": "Booking not found", "success": False}
        
        # Free up the seat if booking was confirmed
        if booking.status == "CONFIRMED":
            # Find the seat for this booking's train and mark as available
            first_unavailable_seat = db.query(models.Seat).filter(
                models.Seat.train_id == booking.train_id,
                models.Seat.is_available == False
            ).first()
            
            if first_unavailable_seat:
                first_unavailable_seat.is_available = True
                db.commit()
        
        # Delete the booking
        db.delete(booking)
        db.commit()
        
        return {"message": "Booking cancelled successfully", "success": True}
    except Exception as e:
        return {"message": str(e), "success": False}

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize sample data if database is empty
db = SessionLocal()
if db.query(models.Train).count() == 0:
    # Add sample trains
    trains = [
        models.Train(train_name="Express 1"),
        models.Train(train_name="Express 2"),
        models.Train(train_name="Express 3"),
    ]
    db.add_all(trains)
    db.commit()
    
    # Add sample seats for each train
    for train in trains:
        for seat_num in range(1, 21):  # 20 seats per train
            seat_type = "aisle" if seat_num % 3 == 0 else ("window" if seat_num % 3 == 1 else "middle")
            berth_type = "lower" if seat_num % 3 == 0 else ("upper" if seat_num % 3 == 1 else "middle")
            seat = models.Seat(
                train_id=train.train_id,
                seat_type=seat_type,
                berth_type=berth_type,
                is_available=True
            )
            db.add(seat)
    db.commit()
db.close()