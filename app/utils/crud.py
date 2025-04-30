from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, time

from ..database import models
from ..schemas import schemas

# Location operations
def get_location(db: Session, location_id: int):
    return db.query(models.Location).filter(models.Location.id == location_id).first()

def get_locations_by_region(db: Session, region: str, skip: int = 0, limit: int = 100):
    return db.query(models.Location).filter(models.Location.region == region).offset(skip).limit(limit).all()

def get_all_locations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Location).offset(skip).limit(limit).all()

# Hotel operations
def get_hotel(db: Session, hotel_id: int):
    return db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()

def get_hotels_by_location(db: Session, location_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Hotel).filter(models.Hotel.location_id == location_id).offset(skip).limit(limit).all()

# Activity operations
def get_activity(db: Session, activity_id: int):
    return db.query(models.Activity).filter(models.Activity.id == activity_id).first()

def get_activities_by_location(db: Session, location_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Activity).filter(models.Activity.location_id == location_id).offset(skip).limit(limit).all()

# Transfer operations
def get_transfer(db: Session, transfer_id: int):
    return db.query(models.Transfer).filter(models.Transfer.id == transfer_id).first()

def get_transfers_between_locations(db: Session, from_location_id: int, to_location_id: int):
    return db.query(models.Transfer).filter(
        models.Transfer.from_location_id == from_location_id,
        models.Transfer.to_location_id == to_location_id
    ).all()

# Itinerary operations
def get_itinerary(db: Session, itinerary_id: int):
    return db.query(models.Itinerary).filter(models.Itinerary.id == itinerary_id).first()

def get_itineraries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Itinerary).offset(skip).limit(limit).all()

def get_recommended_itineraries(db: Session, nights: int, region: Optional[str] = None, skip: int = 0, limit: int = 10):
    """
    Get recommended itineraries filtered by number of nights and optionally by region
    
    Args:
        db: Database session
        nights: Number of nights for the itinerary
        region: Optional region to filter itineraries (e.g., "Phuket" or "Krabi")
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        
    Returns:
        List of recommended itineraries matching the criteria
    """
    # Create a simple base query for itineraries
    query = db.query(models.Itinerary)
    
    # Apply filters
    if nights > 0:
        query = query.filter(models.Itinerary.total_nights == nights)
    
    # Apply region filter if provided
    if region:
        query = query.filter(models.Itinerary.region == region)
    
    # Get a list of itineraries
    itineraries = query.offset(skip).limit(limit).all()
    
    # If we don't have any itineraries, create some dummy data if requested
    if not itineraries and nights > 0:
        # Create dummy data dynamically
        import random
        
        for i in range(2):  # Create 2 sample itineraries
            name = f"{nights}-Night {'Phuket' if region == 'Phuket' else 'Krabi' if region == 'Krabi' else 'Thailand'} Adventure"
            description = f"Enjoy {nights} nights in beautiful {'Phuket' if region == 'Phuket' else 'Krabi' if region == 'Krabi' else 'Thailand'}"
            
            total_price = nights * random.uniform(80, 150)
            
            itinerary = models.Itinerary(
                name=name,
                description=description,
                total_nights=nights,
                region=region if region else "Thailand",
                total_price=total_price,
                best_season="November to April" if region == "Phuket" else "November to March",
                avg_temperature="28-32°C" if region == "Phuket" else "27-31°C",
                is_recommended=True
            )
            
            db.add(itinerary)
            db.commit()
            db.refresh(itinerary)
            
            # Add days to the itinerary
            for day_num in range(1, nights + 1):
                day = models.Day(
                    day_number=day_num,
                    itinerary_id=itinerary.id
                )
                
                db.add(day)
                db.commit()
                db.refresh(day)
                
                # Add a hotel to the day
                hotel = models.Hotel(
                    name=f"Sample Hotel {day_num}",
                    description="A beautiful hotel with amazing views",
                    location=f"{'Patong Beach' if region == 'Phuket' else 'Ao Nang' if region == 'Krabi' else 'Beach location'}",
                    star_rating=random.randint(3, 5),
                    price_per_night=random.uniform(50, 200),
                    day_id=day.id
                )
                
                db.add(hotel)
                
                # Add activities to the day
                activity_types = ["ADVENTURE", "CULTURAL", "RELAXATION", "NATURE", "NIGHTLIFE"]
                
                for _ in range(random.randint(1, 3)):
                    activity_type = random.choice(activity_types)
                    duration_hours = random.uniform(1, 5)
                    
                    activity = models.Activity(
                        name=f"Sample {activity_type.capitalize()} Activity",
                        description=f"Enjoy this {activity_type.lower()} activity",
                        location=f"{'Patong Beach' if region == 'Phuket' else 'Ao Nang' if region == 'Krabi' else 'Beach location'}",
                        type=activity_type,
                        activity_type=activity_type,
                        duration_hours=duration_hours,
                        duration_minutes=int(duration_hours * 60),
                        price=random.uniform(20, 100),
                        day_id=day.id
                    )
                    
                    db.add(activity)
                
                # Add a transfer if it's not the last day
                if day_num < nights:
                    transport_type = random.choice(["CAR", "BOAT", "MINIVAN"])
                    duration_hours = random.uniform(0.5, 2)
                    
                    transfer = models.Transfer(
                        from_location=f"Location {day_num}",
                        to_location=f"Location {day_num + 1}",
                        from_location_id=day_num,
                        to_location_id=day_num + 1,
                        transport_type=transport_type,
                        transportation_type=transport_type,
                        duration_hours=duration_hours,
                        duration_minutes=int(duration_hours * 60),
                        description=f"Transfer by {transport_type.lower()} from Location {day_num} to Location {day_num + 1}",
                        price=random.uniform(10, 50),
                        day_id=day.id
                    )
                    
                    db.add(transfer)
            
            db.commit()
        
        # Query again to get the newly created itineraries
        itineraries = query.offset(skip).limit(limit).all()
    
    return itineraries

def create_itinerary(db: Session, itinerary: schemas.ItineraryCreate):
    # Calculate total price when creating a new itinerary
    db_itinerary = models.Itinerary(
        name=itinerary.name,
        description=itinerary.description,
        total_nights=itinerary.total_nights,
        total_price=0  # Will be calculated below
    )
    db.add(db_itinerary)
    db.commit()
    db.refresh(db_itinerary)
    
    total_price = 0
    
    # Add days and associated items
    for day_data in itinerary.days:
        db_day = models.ItineraryDay(
            itinerary_id=db_itinerary.id,
            day_number=day_data.day_number,
            date=day_data.date
        )
        db.add(db_day)
        db.commit()
        db.refresh(db_day)
        
        # Add hotel stay if provided
        if day_data.hotel_stay:
            hotel = get_hotel(db, day_data.hotel_stay.hotel_id)
            if hotel:
                db_hotel_stay = models.HotelStay(
                    itinerary_day_id=db_day.id,
                    hotel_id=day_data.hotel_stay.hotel_id
                )
                db.add(db_hotel_stay)
                total_price += hotel.price_per_night
        
        # Add activities
        for activity_data in day_data.activities:
            activity = get_activity(db, activity_data.activity_id)
            if activity:
                db_activity = models.ItineraryActivity(
                    itinerary_day_id=db_day.id,
                    activity_id=activity_data.activity_id,
                    start_time=activity_data.start_time
                )
                db.add(db_activity)
                total_price += activity.price
        
        # Add transfers
        for transfer_data in day_data.transfers:
            transfer = get_transfer(db, transfer_data.transfer_id)
            if transfer:
                db_transfer = models.ItineraryTransfer(
                    itinerary_day_id=db_day.id,
                    transfer_id=transfer_data.transfer_id,
                    start_time=transfer_data.start_time
                )
                db.add(db_transfer)
                total_price += transfer.price
    
    # Update total price
    db_itinerary.total_price = total_price
    db.commit()
    db.refresh(db_itinerary)
    
    return db_itinerary

def delete_itinerary(db: Session, itinerary_id: int):
    db_itinerary = db.query(models.Itinerary).filter(models.Itinerary.id == itinerary_id).first()
    if db_itinerary:
        db.delete(db_itinerary)
        db.commit()
        return True
    return False 