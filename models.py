from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base

class Passenger(Base):
    __tablename__ = "passengers"
    passenger_id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

class Train(Base):
    __tablename__ = "trains"
    train_id = Column(Integer, primary_key=True)
    train_name = Column(String)

class Seat(Base):
    __tablename__ = "seats"
    seat_id = Column(Integer, primary_key=True)
    train_id = Column(Integer, ForeignKey("trains.train_id"))
    is_available = Column(Boolean, default=True)

class Booking(Base):
    __tablename__ = "bookings"
    booking_id = Column(Integer, primary_key=True)
    passenger_id = Column(Integer, ForeignKey("passengers.passenger_id"))
    train_id = Column(Integer, ForeignKey("trains.train_id"))
    status = Column(String)