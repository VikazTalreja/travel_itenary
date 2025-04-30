from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Text, Enum
from sqlalchemy.orm import relationship
import enum

from app.database.database import Base

class TransportationType(str, enum.Enum):
    CAR = "CAR"
    BOAT = "BOAT"
    PLANE = "PLANE"
    BUS = "BUS"
    TRAIN = "TRAIN"
    MINIVAN = "MINIVAN"

class ActivityType(str, enum.Enum):
    ADVENTURE = "ADVENTURE"
    CULTURAL = "CULTURAL"
    RELAXATION = "RELAXATION"
    NATURE = "NATURE"
    NIGHTLIFE = "NIGHTLIFE"
    FAMILY = "FAMILY"
    ROMANTIC = "ROMANTIC"
    SHOPPING = "SHOPPING"
    SIGHTSEEING = "SIGHTSEEING"
    FOOD = "FOOD"

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    region = Column(String, index=True)
    
    # Relationships
    hotels = relationship("Hotel", back_populates="location_rel")
    activities = relationship("Activity", back_populates="location_rel")

class Itinerary(Base):
    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    total_nights = Column(Integer)
    total_price = Column(Float)
    region = Column(String, index=True)
    best_season = Column(String, nullable=True)
    avg_temperature = Column(String, nullable=True)
    is_recommended = Column(Boolean, default=True)
    
    # Relationships
    days = relationship("Day", back_populates="itinerary", cascade="all, delete-orphan")

class Day(Base):
    __tablename__ = "days"

    id = Column(Integer, primary_key=True, index=True)
    day_number = Column(Integer)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"))
    
    # Relationships
    itinerary = relationship("Itinerary", back_populates="days")
    hotel = relationship("Hotel", back_populates="day", uselist=False, cascade="all, delete-orphan")
    activities = relationship("Activity", back_populates="day", cascade="all, delete-orphan")
    transfers = relationship("Transfer", back_populates="day", cascade="all, delete-orphan")

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    location = Column(String)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    star_rating = Column(Integer)
    price_per_night = Column(Float)
    day_id = Column(Integer, ForeignKey("days.id"), nullable=True)
    
    # Relationships
    location_rel = relationship("Location", back_populates="hotels", foreign_keys=[location_id])
    day = relationship("Day", back_populates="hotel", foreign_keys=[day_id])

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    location = Column(String)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    type = Column(String, index=True)  # ADVENTURE, CULTURAL, RELAXATION, etc.
    activity_type = Column(String, index=True, nullable=True)  # For schema compatibility
    duration_hours = Column(Float)
    duration_minutes = Column(Integer, nullable=True)  # For schema compatibility
    price = Column(Float)
    day_id = Column(Integer, ForeignKey("days.id"), nullable=True)
    
    # Relationships
    location_rel = relationship("Location", back_populates="activities", foreign_keys=[location_id])
    day = relationship("Day", back_populates="activities", foreign_keys=[day_id])

class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(Integer, primary_key=True, index=True)
    from_location = Column(String)
    to_location = Column(String)
    from_location_id = Column(Integer, nullable=True)  # For schema compatibility
    to_location_id = Column(Integer, nullable=True)  # For schema compatibility
    transport_type = Column(String)  # CAR, BOAT, PLANE, etc.
    transportation_type = Column(String, nullable=True)  # For schema compatibility
    duration_hours = Column(Float)
    duration_minutes = Column(Integer, nullable=True)  # For schema compatibility
    description = Column(Text, nullable=True)  # For schema compatibility
    price = Column(Float)
    day_id = Column(Integer, ForeignKey("days.id"), nullable=True)
    
    # Relationships
    day = relationship("Day", back_populates="transfers")

class ItineraryFeedback(Base):
    __tablename__ = "itinerary_feedback"

    id = Column(Integer, primary_key=True, index=True)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"))
    rating = Column(Integer)  # 1-5 stars
    comments = Column(Text, nullable=True)
    
    # Relationships
    itinerary = relationship("Itinerary") 