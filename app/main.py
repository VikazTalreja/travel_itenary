from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

from .database.database import engine, get_db
from .database import models
from .schemas import schemas
from .utils import crud

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Travel Itinerary API",
    description="API for managing travel itineraries for Phuket and Krabi regions",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Travel Itinerary API"}

@app.get("/api/itineraries", response_model=schemas.ItineraryResponse)
async def get_all_itineraries(
    skip: int = 0, 
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get all itineraries with pagination
    """
    itineraries = crud.get_itineraries(db, skip=skip, limit=limit)
    
    # Convert to dictionaries for response
    result_itineraries = []
    for itinerary in itineraries:
        result_days = []
        for day in itinerary.days:
            # Process hotel
            hotel_data = None
            if day.hotel:
                hotel_data = {
                    "id": day.hotel.id,
                    "name": day.hotel.name,
                    "description": day.hotel.description,
                    "location": day.hotel.location,
                    "location_id": day.hotel.location_id or 0,
                    "star_rating": day.hotel.star_rating,
                    "price_per_night": day.hotel.price_per_night
                }
            
            # Process activities
            activities_data = []
            for activity in day.activities:
                activities_data.append({
                    "id": activity.id,
                    "name": activity.name,
                    "description": activity.description,
                    "location": activity.location,
                    "location_id": activity.location_id or 0,
                    "activity_type": activity.activity_type or activity.type,
                    "duration_minutes": activity.duration_minutes or int(activity.duration_hours * 60),
                    "price": activity.price
                })
            
            # Process transfers
            transfers_data = []
            for transfer in day.transfers:
                transfers_data.append({
                    "id": transfer.id,
                    "from_location": transfer.from_location,
                    "to_location": transfer.to_location,
                    "from_location_id": transfer.from_location_id or 0,
                    "to_location_id": transfer.to_location_id or 0,
                    "transportation_type": transfer.transportation_type or transfer.transport_type,
                    "duration_minutes": transfer.duration_minutes or int(transfer.duration_hours * 60),
                    "description": transfer.description or f"Transfer from {transfer.from_location} to {transfer.to_location}",
                    "price": transfer.price
                })
            
            result_days.append({
                "id": day.id,
                "day_number": day.day_number,
                "itinerary_id": day.itinerary_id,
                "hotel": hotel_data,
                "activities": activities_data,
                "transfers": transfers_data
            })
        
        result_itineraries.append({
            "id": itinerary.id,
            "name": itinerary.name,
            "description": itinerary.description,
            "total_nights": itinerary.total_nights,
            "total_price": itinerary.total_price,
            "region": itinerary.region,
            "best_season": itinerary.best_season,
            "avg_temperature": itinerary.avg_temperature,
            "is_recommended": itinerary.is_recommended,
            "days": result_days
        })
    
    return {
        "success": True,
        "data": result_itineraries,
        "message": f"Retrieved {len(itineraries)} itineraries"
    }

@app.get("/api/itineraries/{itinerary_id}", response_model=schemas.ItineraryResponse)
async def get_itinerary(itinerary_id: int, db: Session = Depends(get_db)):
    """
    Get a specific itinerary by ID
    """
    itinerary = crud.get_itinerary(db, itinerary_id=itinerary_id)
    if itinerary is None:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    
    # Convert to dictionary for response
    result_days = []
    for day in itinerary.days:
        # Process hotel
        hotel_data = None
        if day.hotel:
            hotel_data = {
                "id": day.hotel.id,
                "name": day.hotel.name,
                "description": day.hotel.description,
                "location": day.hotel.location,
                "location_id": day.hotel.location_id or 0,
                "star_rating": day.hotel.star_rating,
                "price_per_night": day.hotel.price_per_night
            }
        
        # Process activities
        activities_data = []
        for activity in day.activities:
            activities_data.append({
                "id": activity.id,
                "name": activity.name,
                "description": activity.description,
                "location": activity.location,
                "location_id": activity.location_id or 0,
                "activity_type": activity.activity_type or activity.type,
                "duration_minutes": activity.duration_minutes or int(activity.duration_hours * 60),
                "price": activity.price
            })
        
        # Process transfers
        transfers_data = []
        for transfer in day.transfers:
            transfers_data.append({
                "id": transfer.id,
                "from_location": transfer.from_location,
                "to_location": transfer.to_location,
                "from_location_id": transfer.from_location_id or 0,
                "to_location_id": transfer.to_location_id or 0,
                "transportation_type": transfer.transportation_type or transfer.transport_type,
                "duration_minutes": transfer.duration_minutes or int(transfer.duration_hours * 60),
                "description": transfer.description or f"Transfer from {transfer.from_location} to {transfer.to_location}",
                "price": transfer.price
            })
        
        result_days.append({
            "id": day.id,
            "day_number": day.day_number,
            "itinerary_id": day.itinerary_id,
            "hotel": hotel_data,
            "activities": activities_data,
            "transfers": transfers_data
        })
    
    result_itinerary = {
        "id": itinerary.id,
        "name": itinerary.name,
        "description": itinerary.description,
        "total_nights": itinerary.total_nights,
        "total_price": itinerary.total_price,
        "region": itinerary.region,
        "best_season": itinerary.best_season,
        "avg_temperature": itinerary.avg_temperature,
        "is_recommended": itinerary.is_recommended,
        "days": result_days
    }
    
    return {
        "success": True,
        "data": result_itinerary,
        "message": f"Retrieved itinerary with ID {itinerary_id}"
    }

@app.post("/api/itineraries", response_model=schemas.ItineraryResponse, status_code=status.HTTP_201_CREATED)
async def create_itinerary(itinerary: schemas.ItineraryCreate, db: Session = Depends(get_db)):
    """
    Create a new itinerary
    """
    db_itinerary = crud.create_itinerary(db, itinerary=itinerary)
    
    # Convert to dictionary for response
    result_days = []
    for day in db_itinerary.days:
        # Process hotel
        hotel_data = None
        if day.hotel:
            hotel_data = {
                "id": day.hotel.id,
                "name": day.hotel.name,
                "description": day.hotel.description,
                "location": day.hotel.location,
                "location_id": day.hotel.location_id or 0,
                "star_rating": day.hotel.star_rating,
                "price_per_night": day.hotel.price_per_night
            }
        
        # Process activities
        activities_data = []
        for activity in day.activities:
            activities_data.append({
                "id": activity.id,
                "name": activity.name,
                "description": activity.description,
                "location": activity.location,
                "location_id": activity.location_id or 0,
                "activity_type": activity.activity_type or activity.type,
                "duration_minutes": activity.duration_minutes or int(activity.duration_hours * 60),
                "price": activity.price
            })
        
        # Process transfers
        transfers_data = []
        for transfer in day.transfers:
            transfers_data.append({
                "id": transfer.id,
                "from_location": transfer.from_location,
                "to_location": transfer.to_location,
                "from_location_id": transfer.from_location_id or 0,
                "to_location_id": transfer.to_location_id or 0,
                "transportation_type": transfer.transportation_type or transfer.transport_type,
                "duration_minutes": transfer.duration_minutes or int(transfer.duration_hours * 60),
                "description": transfer.description or f"Transfer from {transfer.from_location} to {transfer.to_location}",
                "price": transfer.price
            })
        
        result_days.append({
            "id": day.id,
            "day_number": day.day_number,
            "itinerary_id": day.itinerary_id,
            "hotel": hotel_data,
            "activities": activities_data,
            "transfers": transfers_data
        })
    
    result_itinerary = {
        "id": db_itinerary.id,
        "name": db_itinerary.name,
        "description": db_itinerary.description,
        "total_nights": db_itinerary.total_nights,
        "total_price": db_itinerary.total_price,
        "region": db_itinerary.region,
        "best_season": db_itinerary.best_season,
        "avg_temperature": db_itinerary.avg_temperature,
        "is_recommended": db_itinerary.is_recommended,
        "days": result_days
    }
    
    return {
        "success": True,
        "data": result_itinerary,
        "message": "Itinerary created successfully"
    }

@app.get("/api/recommended-itineraries", response_model=schemas.ItineraryResponse)
async def get_recommended_itineraries(
    nights: int, 
    region: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    """
    Get recommended itineraries for a specific number of nights
    """
    if nights < 2 or nights > 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Number of nights must be between 2 and 8"
        )
    
    # Get from database directly
    itineraries = crud.get_recommended_itineraries(db, nights=nights, region=region)
    
    # Convert to dictionaries for response
    result_itineraries = []
    for itinerary in itineraries:
        result_days = []
        for day in itinerary.days:
            # Process hotel
            hotel_data = None
            if day.hotel:
                hotel_data = {
                    "id": day.hotel.id,
                    "name": day.hotel.name,
                    "description": day.hotel.description,
                    "location": day.hotel.location,
                    "location_id": day.hotel.location_id or 0,
                    "star_rating": day.hotel.star_rating,
                    "price_per_night": day.hotel.price_per_night
                }
            
            # Process activities
            activities_data = []
            for activity in day.activities:
                activities_data.append({
                    "id": activity.id,
                    "name": activity.name,
                    "description": activity.description,
                    "location": activity.location,
                    "location_id": activity.location_id or 0,
                    "activity_type": activity.activity_type or activity.type,
                    "duration_minutes": activity.duration_minutes or int(activity.duration_hours * 60),
                    "price": activity.price
                })
            
            # Process transfers
            transfers_data = []
            for transfer in day.transfers:
                transfers_data.append({
                    "id": transfer.id,
                    "from_location": transfer.from_location,
                    "to_location": transfer.to_location,
                    "from_location_id": transfer.from_location_id or 0,
                    "to_location_id": transfer.to_location_id or 0,
                    "transportation_type": transfer.transportation_type or transfer.transport_type,
                    "duration_minutes": transfer.duration_minutes or int(transfer.duration_hours * 60),
                    "description": transfer.description or f"Transfer from {transfer.from_location} to {transfer.to_location}",
                    "price": transfer.price
                })
            
            result_days.append({
                "id": day.id,
                "day_number": day.day_number,
                "itinerary_id": day.itinerary_id,
                "hotel": hotel_data,
                "activities": activities_data,
                "transfers": transfers_data
            })
        
        result_itineraries.append({
            "id": itinerary.id,
            "name": itinerary.name,
            "description": itinerary.description,
            "total_nights": itinerary.total_nights,
            "total_price": itinerary.total_price,
            "region": itinerary.region,
            "best_season": itinerary.best_season,
            "avg_temperature": itinerary.avg_temperature,
            "is_recommended": itinerary.is_recommended,
            "days": result_days
        })
    
    return {
        "success": True,
        "data": result_itineraries,
        "message": f"Retrieved {len(itineraries)} recommended itineraries for {nights} nights"
    }

@app.get("/api/mcp/recommended-itineraries", response_model=schemas.ItineraryResponse)
async def get_mcp_recommended_itineraries(
    nights: int, 
    region: Optional[str] = None,
    interests: Optional[str] = None,  # comma-separated list of interests
    db: Session = Depends(get_db)
):
    """
    Get recommended itineraries for MCP server based on filters
    """
    try:
        # Check if nights is valid
        if nights < 1 or nights > 14:
            nights = 3  # Set a default value if invalid
        
        # Parse interests if provided
        interest_list = None
        if interests:
            interest_list = [interest.strip() for interest in interests.split(",")]
        
        # Get itineraries - this will create them if none exist
        itineraries = crud.get_recommended_itineraries(
            db, 
            nights=nights, 
            region=region,
            limit=5  # Limit to 5 itineraries
        )
        
        # If we have interests, filter results that match those interests
        if interest_list and len(interest_list) > 0 and len(itineraries) > 0:
            # Simple filtering
            filtered_itineraries = []
            for itinerary in itineraries:
                matches_interests = False
                
                # Check each day's activities
                for day in itinerary.days:
                    for activity in day.activities:
                        # If the activity type matches any of the requested interests
                        if activity.type in interest_list:
                            matches_interests = True
                            break
                    if matches_interests:
                        break
                
                if matches_interests:
                    filtered_itineraries.append(itinerary)
            
            # Only use filtered results if we found any
            if filtered_itineraries:
                itineraries = filtered_itineraries
        
        # Manually create a dictionary representation of the itineraries compatible with the Pydantic schema
        result_itineraries = []
        for itinerary in itineraries:
            result_days = []
            for day in itinerary.days:
                # Process hotel
                hotel_data = None
                if day.hotel:
                    hotel_data = {
                        "id": day.hotel.id,
                        "name": day.hotel.name,
                        "description": day.hotel.description,
                        "location": day.hotel.location,
                        "location_id": day.hotel.location_id or 0,
                        "star_rating": day.hotel.star_rating,
                        "price_per_night": day.hotel.price_per_night
                    }
                
                # Process activities
                activities_data = []
                for activity in day.activities:
                    activities_data.append({
                        "id": activity.id,
                        "name": activity.name,
                        "description": activity.description,
                        "location": activity.location,
                        "location_id": activity.location_id or 0,
                        "activity_type": activity.activity_type or activity.type,
                        "duration_minutes": activity.duration_minutes or int(activity.duration_hours * 60),
                        "price": activity.price
                    })
                
                # Process transfers
                transfers_data = []
                for transfer in day.transfers:
                    transfers_data.append({
                        "id": transfer.id,
                        "from_location": transfer.from_location,
                        "to_location": transfer.to_location,
                        "from_location_id": transfer.from_location_id or 0,
                        "to_location_id": transfer.to_location_id or 0,
                        "transportation_type": transfer.transportation_type or transfer.transport_type,
                        "duration_minutes": transfer.duration_minutes or int(transfer.duration_hours * 60),
                        "description": transfer.description or f"Transfer from {transfer.from_location} to {transfer.to_location}",
                        "price": transfer.price
                    })
                
                result_days.append({
                    "id": day.id,
                    "day_number": day.day_number,
                    "itinerary_id": day.itinerary_id,
                    "hotel": hotel_data,
                    "activities": activities_data,
                    "transfers": transfers_data
                })
            
            result_itineraries.append({
                "id": itinerary.id,
                "name": itinerary.name,
                "description": itinerary.description,
                "total_nights": itinerary.total_nights,
                "total_price": itinerary.total_price,
                "region": itinerary.region,
                "best_season": itinerary.best_season,
                "avg_temperature": itinerary.avg_temperature,
                "is_recommended": itinerary.is_recommended,
                "days": result_days
            })
        
        return {
            "success": True,
            "data": result_itineraries,
            "message": f"Retrieved {len(itineraries)} recommended itineraries for {nights} nights"
        }
    except Exception as e:
        import traceback
        print(f"Error generating recommendations: {str(e)}")
        print(traceback.format_exc())
        
        # Return a more detailed error message for debugging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating recommendations: {str(e)}"
        )

@app.post("/api/mcp/feedback", response_model=schemas.FeedbackResponse)
async def send_itinerary_feedback(
    feedback: schemas.ItineraryFeedback, 
    db: Session = Depends(get_db)
):
    """
    Save feedback about an itinerary
    """
    try:
        # Check if itinerary exists
        itinerary = crud.get_itinerary(db, feedback.itinerary_id)
        if not itinerary:
            return {
                "success": False,
                "message": f"Itinerary with ID {feedback.itinerary_id} not found"
            }
        
        # Save feedback to database
        new_feedback = models.ItineraryFeedback(
            itinerary_id=feedback.itinerary_id,
            rating=feedback.rating,
            comments=feedback.comments
        )
        
        db.add(new_feedback)
        db.commit()
        
        return {
            "success": True,
            "message": f"Feedback for itinerary {feedback.itinerary_id} saved successfully"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving feedback: {str(e)}"
        )

@app.get("/api/seed-database")
async def seed_database():
    """
    Initialize or reset the database with sample data
    """
    try:
        from app.database.seed import seed_database
        seed_database()
        return {
            "success": True,
            "message": "Database seeded successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error seeding database: {str(e)}"
        )
    
@app.post("/api/generate-ai-itinerary", response_model=schemas.ItineraryResponse)
async def generate_ai_itinerary(
    request: schemas.AIItineraryRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a custom itinerary using AI
    """
    try:
        # Create a new itinerary
        new_itinerary = models.Itinerary(
            name=f"Custom {request.nights}-Night {request.region} Itinerary",
            description=f"A personalized itinerary for {request.nights} nights in {request.region}. "
                      f"Budget level: {request.budget}. "
                      f"Interests: {', '.join(request.interests) if request.interests else 'Various activities'}. "
                      f"{request.special_requests if request.special_requests else ''}",
            total_nights=request.nights,
            region=request.region,
            total_price=0.0,
            best_season="November to April" if request.region == "Phuket" else "November to March",
            avg_temperature="28-32°C" if request.region == "Phuket" else "27-31°C",
            is_recommended=True
        )
        
        db.add(new_itinerary)
        db.commit()
        db.refresh(new_itinerary)
        
        # Get sample hotels, activities, and transfers to create the itinerary
        hotels = db.query(models.Hotel).join(models.Location).filter(
            models.Location.region == request.region
        ).all()
        
        activities = db.query(models.Activity).join(models.Location).filter(
            models.Location.region == request.region
        ).all()
        
        if request.interests:
            filtered_activities = [a for a in activities if a.activity_type in request.interests]
            # If we have matching activities, use them; otherwise use all activities
            if filtered_activities:
                activities = filtered_activities
        
        price_factor = 0.7 if request.budget == "Budget" else (1.3 if request.budget == "Luxury" else 1.0)
        
        total_price = 0
        
        # Create days
        import random
        for day_num in range(1, request.nights + 1):
            new_day = models.Day(
                day_number=day_num,
                itinerary_id=new_itinerary.id,
            )
            db.add(new_day)
            db.commit()
            db.refresh(new_day)
            
            # Add hotel
            if hotels:
                hotel = random.choice(hotels)
                adjusted_price = hotel.price_per_night * price_factor
                
                new_hotel = models.Hotel(
                    name=hotel.name,
                    description=hotel.description,
                    location=hotel.location,
                    star_rating=hotel.star_rating,
                    price_per_night=adjusted_price,
                    day_id=new_day.id
                )
                db.add(new_hotel)
                total_price += adjusted_price
            
            # Add 2-3 activities per day
            day_activities = []
            if activities:
                day_activities = random.sample(activities, min(3, len(activities)))
                
                for activity in day_activities:
                    adjusted_price = activity.price * price_factor
                    
                    new_activity = models.Activity(
                        name=activity.name,
                        description=activity.description,
                        location=activity.location,
                        type=activity.type,  
                        activity_type=activity.type,
                        duration_hours=activity.duration_hours,
                        duration_minutes=int(activity.duration_hours * 60),
                        price=adjusted_price,
                        day_id=new_day.id
                    )
                    db.add(new_activity)
                    total_price += adjusted_price
            
            # Add transfers if not the last day
            if day_num < request.nights and hotels and len(hotels) > 1:
                from_hotel = hotels[day_num % len(hotels)]
                to_hotel = hotels[(day_num + 1) % len(hotels)]
                
                transport_types = ["CAR", "BOAT", "MINIVAN", "BUS"]
                transport_type = random.choice(transport_types)
                duration = random.uniform(0.5, 2.0)  # 30 mins to 2 hours
                transfer_price = (25 + random.uniform(10, 40)) * price_factor
                
                new_transfer = models.Transfer(
                    from_location=from_hotel.location,
                    to_location=to_hotel.location,
                    from_location_id=day_num,
                    to_location_id=day_num + 1,
                    transport_type=transport_type,
                    transportation_type=transport_type,
                    duration_hours=duration,
                    duration_minutes=int(duration * 60),
                    description=f"Transfer by {transport_type.lower()} from {from_hotel.location} to {to_hotel.location}",
                    price=transfer_price,
                    day_id=new_day.id
                )
                db.add(new_transfer)
                total_price += transfer_price
        
        # Update the total price
        new_itinerary.total_price = total_price
        db.commit()
        db.refresh(new_itinerary)
        
        # Manually create a dictionary representation of the itinerary compatible with the Pydantic schema
        result_days = []
        for day in new_itinerary.days:
            # Process hotel
            hotel_data = None
            if day.hotel:
                hotel_data = {
                    "id": day.hotel.id,
                    "name": day.hotel.name,
                    "description": day.hotel.description,
                    "location": day.hotel.location,
                    "location_id": day.hotel.location_id or 0,
                    "star_rating": day.hotel.star_rating,
                    "price_per_night": day.hotel.price_per_night
                }
            
            # Process activities
            activities_data = []
            for activity in day.activities:
                activities_data.append({
                    "id": activity.id,
                    "name": activity.name,
                    "description": activity.description,
                    "location": activity.location,
                    "location_id": activity.location_id or 0,
                    "activity_type": activity.activity_type or activity.type,
                    "duration_minutes": activity.duration_minutes or int(activity.duration_hours * 60),
                    "price": activity.price
                })
            
            # Process transfers
            transfers_data = []
            for transfer in day.transfers:
                transfers_data.append({
                    "id": transfer.id,
                    "from_location": transfer.from_location,
                    "to_location": transfer.to_location,
                    "from_location_id": transfer.from_location_id or 0,
                    "to_location_id": transfer.to_location_id or 0,
                    "transportation_type": transfer.transportation_type or transfer.transport_type,
                    "duration_minutes": transfer.duration_minutes or int(transfer.duration_hours * 60),
                    "description": transfer.description or f"Transfer from {transfer.from_location} to {transfer.to_location}",
                    "price": transfer.price
                })
            
            result_days.append({
                "id": day.id,
                "day_number": day.day_number,
                "itinerary_id": day.itinerary_id,
                "hotel": hotel_data,
                "activities": activities_data,
                "transfers": transfers_data
            })
        
        result_itinerary = {
            "id": new_itinerary.id,
            "name": new_itinerary.name,
            "description": new_itinerary.description,
            "total_nights": new_itinerary.total_nights,
            "total_price": new_itinerary.total_price,
            "region": new_itinerary.region,
            "best_season": new_itinerary.best_season,
            "avg_temperature": new_itinerary.avg_temperature,
            "is_recommended": new_itinerary.is_recommended,
            "days": result_days
        }
        
        return {
            "success": True,
            "data": result_itinerary,
            "message": f"Generated a custom {request.nights}-night itinerary for {request.region}"
        }
    except Exception as e:
        db.rollback()
        import traceback
        print(f"Error generating AI itinerary: {str(e)}")
        print(traceback.format_exc())
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating AI itinerary: {str(e)}"
        )

@app.post("/api/mcp/custom-itinerary", response_model=schemas.ItineraryResponse)
async def generate_mcp_custom_itinerary(
    request: schemas.AIItineraryRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a custom itinerary using AI for MCP interface
    """
    # This is the same as generate_ai_itinerary but with a different route
    return await generate_ai_itinerary(request, db)

@app.get("/api/mcp/quick-recommendation", response_model=schemas.ItineraryResponse)
async def get_mcp_quick_recommendation(
    nights: int, 
    db: Session = Depends(get_db)
):
    """
    Get a quick recommendation based only on the number of nights
    """
    # Use the existing endpoint but simplify the call
    return await get_mcp_recommended_itineraries(nights=nights, db=db)

@app.get("/api/mcp/itinerary/{itinerary_id}", response_model=schemas.ItineraryResponse)
async def get_mcp_itinerary_details(
    itinerary_id: int, 
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific itinerary
    """
    try:
        itinerary = crud.get_itinerary(db, itinerary_id)
        if not itinerary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Itinerary with ID {itinerary_id} not found"
            )
        
        # Manually create a dictionary representation of the itinerary compatible with the Pydantic schema
        result_days = []
        for day in itinerary.days:
            # Process hotel
            hotel_data = None
            if day.hotel:
                hotel_data = {
                    "id": day.hotel.id,
                    "name": day.hotel.name,
                    "description": day.hotel.description,
                    "location": day.hotel.location,
                    "location_id": day.hotel.location_id or 0,
                    "star_rating": day.hotel.star_rating,
                    "price_per_night": day.hotel.price_per_night
                }
            
            # Process activities
            activities_data = []
            for activity in day.activities:
                activities_data.append({
                    "id": activity.id,
                    "name": activity.name,
                    "description": activity.description,
                    "location": activity.location,
                    "location_id": activity.location_id or 0,
                    "activity_type": activity.activity_type or activity.type,
                    "duration_minutes": activity.duration_minutes or int(activity.duration_hours * 60),
                    "price": activity.price
                })
            
            # Process transfers
            transfers_data = []
            for transfer in day.transfers:
                transfers_data.append({
                    "id": transfer.id,
                    "from_location": transfer.from_location,
                    "to_location": transfer.to_location,
                    "from_location_id": transfer.from_location_id or 0,
                    "to_location_id": transfer.to_location_id or 0,
                    "transportation_type": transfer.transportation_type or transfer.transport_type,
                    "duration_minutes": transfer.duration_minutes or int(transfer.duration_hours * 60),
                    "description": transfer.description or f"Transfer from {transfer.from_location} to {transfer.to_location}",
                    "price": transfer.price
                })
            
            result_days.append({
                "id": day.id,
                "day_number": day.day_number,
                "itinerary_id": day.itinerary_id,
                "hotel": hotel_data,
                "activities": activities_data,
                "transfers": transfers_data
            })
        
        result_itinerary = {
            "id": itinerary.id,
            "name": itinerary.name,
            "description": itinerary.description,
            "total_nights": itinerary.total_nights,
            "total_price": itinerary.total_price,
            "region": itinerary.region,
            "best_season": itinerary.best_season,
            "avg_temperature": itinerary.avg_temperature,
            "is_recommended": itinerary.is_recommended,
            "days": result_days
        }
        
        return {
            "success": True,
            "data": result_itinerary,
            "message": f"Retrieved details for itinerary {itinerary_id}"
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"Error retrieving itinerary details: {str(e)}")
        print(traceback.format_exc())
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving itinerary details: {str(e)}"
        )

@app.post("/api/mcp/feedback", response_model=schemas.FeedbackResponse)
async def send_mcp_itinerary_feedback(
    itinerary_id: int,
    rating: int,
    comments: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Send feedback about a recommended itinerary through MCP
    """
    # Create a feedback object
    feedback = schemas.ItineraryFeedback(
        itinerary_id=itinerary_id,
        rating=rating,
        comments=comments
    )
    
    # Use the existing endpoint
    return await send_itinerary_feedback(feedback, db)

@app.post("/api/ai-itineraries", response_model=schemas.ItineraryResponse)
async def create_ai_itinerary_route(
    request: schemas.AIItineraryRequest,
    db: Session = Depends(get_db)
):
    """
    Generate AI itineraries through the web interface
    """
    # Use the existing generate_ai_itinerary function
    return await generate_ai_itinerary(request, db) 