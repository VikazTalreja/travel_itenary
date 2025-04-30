from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import date, time
from enum import Enum

# Enum classes
class TransportationType(str, Enum):
    CAR = "CAR"
    BOAT = "BOAT"
    PLANE = "PLANE"
    BUS = "BUS"
    TRAIN = "TRAIN"
    MINIVAN = "MINIVAN"

class ActivityType(str, Enum):
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

# Base schemas
class LocationBase(BaseModel):
    name: str
    description: str
    region: str

class HotelBase(BaseModel):
    name: str
    description: str
    star_rating: int
    price_per_night: float
    location_id: int

class TransferBase(BaseModel):
    transportation_type: TransportationType
    from_location_id: int
    to_location_id: int
    duration_minutes: int
    price: float
    description: str

class ActivityBase(BaseModel):
    name: str
    description: str
    activity_type: ActivityType
    duration_minutes: int
    price: float
    location_id: int

# Response schemas
class Location(LocationBase):
    id: int

    model_config = {"from_attributes": True}

class Hotel(HotelBase):
    id: int
    location: Location

    model_config = {"from_attributes": True}

class Transfer(TransferBase):
    id: int
    from_location: Location
    to_location: Location

    model_config = {"from_attributes": True}

class Activity(ActivityBase):
    id: int
    location: Location

    model_config = {"from_attributes": True}

# Itinerary item schemas
class HotelStayBase(BaseModel):
    hotel_id: int

class HotelStay(HotelStayBase):
    id: int
    hotel: Hotel

    model_config = {"from_attributes": True}

class ItineraryActivityBase(BaseModel):
    activity_id: int
    start_time: Optional[time] = None

class ItineraryActivity(ItineraryActivityBase):
    id: int
    activity: Activity

    model_config = {"from_attributes": True}

class ItineraryTransferBase(BaseModel):
    transfer_id: int
    start_time: Optional[time] = None

class ItineraryTransfer(ItineraryTransferBase):
    id: int
    transfer: Transfer

    model_config = {"from_attributes": True}

# Itinerary day schemas
class ItineraryDayBase(BaseModel):
    day_number: int
    date: Optional[date] = None
    hotel_stay: Optional[HotelStayBase] = None
    activities: List[ItineraryActivityBase] = []
    transfers: List[ItineraryTransferBase] = []

class ItineraryDayCreate(ItineraryDayBase):
    pass

class ItineraryDay(ItineraryDayBase):
    id: int
    hotel_stay: Optional[HotelStay] = None
    activities: List[ItineraryActivity] = []
    transfers: List[ItineraryTransfer] = []

    model_config = {"from_attributes": True}

# Main itinerary schemas
class ItineraryBase(BaseModel):
    name: str
    description: str
    total_nights: int
    region: str
    total_price: float
    best_season: Optional[str] = None
    avg_temperature: Optional[str] = None
    is_recommended: Optional[bool] = True

class ItineraryCreate(ItineraryBase):
    days: List[ItineraryDayCreate] = []

class Itinerary(ItineraryBase):
    id: int
    days: List[ItineraryDay] = []

    model_config = {"from_attributes": True}

# Request schemas for the API
class RecommendedItineraryRequest(BaseModel):
    nights: int = Field(..., ge=2, le=8, description="Number of nights (between 2-8)")

# Feedback schema
class ItineraryFeedback(BaseModel):
    itinerary_id: int
    rating: int  # 1-5 stars
    comments: Optional[str] = None

# Response schemas for the API
class ItineraryResponse(BaseModel):
    success: bool
    data: Optional[Union[Itinerary, List[Itinerary]]] = None
    message: str

class ErrorResponse(BaseModel):
    success: bool = False
    error: str

class FeedbackResponse(BaseModel):
    success: bool
    message: str

# AI itinerary request
class AIItineraryRequest(BaseModel):
    nights: int
    region: str
    interests: Optional[List[str]] = None
    budget: Optional[str] = "Standard"
    special_requests: Optional[str] = None

# Base models
class HotelCreate(HotelBase):
    pass

class ActivityCreate(ActivityBase):
    pass

class TransferCreate(TransferBase):
    pass

class DayBase(BaseModel):
    day_number: int

class DayCreate(DayBase):
    hotel: Optional[HotelCreate] = None
    activities: Optional[List[ActivityCreate]] = []
    transfers: Optional[List[TransferCreate]] = []

class ItineraryCreate(ItineraryBase):
    days: List[DayCreate]

class Hotel(HotelBase):
    id: int

    model_config = {"from_attributes": True}

class Activity(ActivityBase):
    id: int

    model_config = {"from_attributes": True}

class Transfer(TransferBase):
    id: int

    model_config = {"from_attributes": True}

class Day(DayBase):
    id: int
    itinerary_id: int
    hotel: Optional[Hotel] = None
    activities: Optional[List[Activity]] = []
    transfers: Optional[List[Transfer]] = []

    model_config = {"from_attributes": True}

class Itinerary(ItineraryBase):
    id: int
    days: List[Day] = []

    model_config = {"from_attributes": True}

class ItineraryResponse(BaseModel):
    success: bool
    data: Optional[Union[Itinerary, List[Itinerary]]] = None
    message: str 