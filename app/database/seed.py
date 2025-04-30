import sys
import os
from sqlalchemy.orm import Session
from datetime import time
import random

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.database.database import SessionLocal, engine
from app.database import models
from app.database.models import TransportationType, ActivityType

def seed_database():
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(models.ItineraryFeedback).delete()
    db.query(models.Transfer).delete()
    db.query(models.Activity).delete()
    db.query(models.Hotel).delete()
        db.query(models.Day).delete()
        db.query(models.Itinerary).delete()
    db.query(models.Location).delete()
    db.commit()

        # Seed locations - Phuket
        phuket_locations = [
            {"name": "Patong", "region": "Phuket", "description": "Bustling beach town with vibrant nightlife and shopping."},
            {"name": "Kata", "region": "Phuket", "description": "Beautiful beach with relaxed atmosphere and family-friendly environment."},
            {"name": "Karon", "region": "Phuket", "description": "Long sandy beach with clear water and plenty of dining options."},
            {"name": "Rawai", "region": "Phuket", "description": "Authentic fishing village with seafood restaurants and local charm."},
            {"name": "Kamala", "region": "Phuket", "description": "Quiet beach town with a relaxed vibe and stunning sunset views."},
            {"name": "Bang Tao", "region": "Phuket", "description": "Long beach with luxury resorts and upscale dining."},
            {"name": "Surin", "region": "Phuket", "description": "Upscale beach area with high-end resorts and beach clubs."},
            {"name": "Chalong", "region": "Phuket", "description": "Major boat harbor with access to nearby islands and diving."},
            {"name": "Mai Khao", "region": "Phuket", "description": "Phuket's longest beach with nature reserves and turtle nesting sites."},
            {"name": "Nai Harn", "region": "Phuket", "description": "Picturesque bay with one of Phuket's best beaches."},
            {"name": "Phuket Town", "region": "Phuket", "description": "Charming old town with Sino-Portuguese architecture and cultural sites."},
            {"name": "Cape Panwa", "region": "Phuket", "description": "Secluded cape with panoramic views and peaceful beaches."},
            {"name": "Nai Yang", "region": "Phuket", "description": "Quiet beach near the airport with a national park."},
            {"name": "Freedom Beach", "region": "Phuket", "description": "Hidden gem with crystal clear water, accessible by boat."},
            {"name": "Kalim", "region": "Phuket", "description": "Rocky beach north of Patong with great surfing spots."},
        ]
        
        # Seed locations - Krabi
        krabi_locations = [
            {"name": "Ao Nang", "region": "Krabi", "description": "Main beach area with shops, restaurants, and access to nearby islands."},
            {"name": "Railay", "region": "Krabi", "description": "Stunning peninsula accessible only by boat, famous for rock climbing."},
            {"name": "Klong Muang", "region": "Krabi", "description": "Quiet beach area with luxury resorts and natural surroundings."},
            {"name": "Krabi Town", "region": "Krabi", "description": "Provincial capital with markets, temples, and authentic Thai culture."},
            {"name": "Tub Kaek", "region": "Krabi", "description": "Secluded beach with views of Hong Islands and luxury resorts."},
            {"name": "Nopparat Thara", "region": "Krabi", "description": "Long beach with shallow water, perfect for families."},
            {"name": "Phra Nang", "region": "Krabi", "description": "Beautiful beach near Railay with a famous cave shrine."},
            {"name": "Koh Lanta", "region": "Krabi", "description": "Laid-back island with beautiful beaches and national park."},
            {"name": "Koh Phi Phi", "region": "Krabi", "description": "Iconic island with stunning beaches and vibrant nightlife."},
            {"name": "Koh Jum", "region": "Krabi", "description": "Quiet, unspoiled island with peaceful beaches and few tourists."},
            {"name": "Ton Sai", "region": "Krabi", "description": "Climber's paradise with a bohemian atmosphere."},
            {"name": "Klong Dao", "region": "Krabi", "description": "Beautiful beach on Koh Lanta with shallow, clear water."},
            {"name": "Pak Nam Krabi", "region": "Krabi", "description": "Fishing village with mangrove forests and viewpoints."},
            {"name": "Thalen Bay", "region": "Krabi", "description": "Peaceful bay with limestone cliffs and emerald waters."},
            {"name": "Ao Luk", "region": "Krabi", "description": "District known for mangrove forests, caves and archaeological sites."},
        ]
        
        # Add locations to database
        db_locations = {}
        for loc_data in phuket_locations + krabi_locations:
            location = models.Location(
                name=loc_data["name"],
                region=loc_data["region"],
                description=loc_data["description"]
            )
            db.add(location)
            db.flush()
            key = f"{loc_data['region']}-{loc_data['name']}"
            db_locations[key] = location
        
    db.commit()

        # Seed hotels
        hotels_data = []
        
        # Phuket hotels
        for i, loc in enumerate(phuket_locations):
            loc_key = f"Phuket-{loc['name']}"
            # Add 2-3 hotels per location
            for j in range(random.randint(2, 3)):
                star_rating = random.randint(3, 5)
                price_base = {3: 50, 4: 100, 5: 200}[star_rating]
                price = price_base + random.randint(-20, 50)
                
                hotel_name = f"{['Sunny', 'Palm', 'Royal', 'Grand', 'Ocean', 'Tropical', 'Emerald', 'Golden', 'Paradise'][random.randint(0, 8)]} {['Resort', 'Hotel', 'Suites', 'Villa', 'Palace', 'Bay Hotel'][random.randint(0, 5)]}"
                
                hotels_data.append({
                    "name": hotel_name,
                    "description": f"A {star_rating}-star hotel located in {loc['name']}, offering comfortable accommodations with beautiful views.",
                    "location": loc["name"],
                    "location_id": db_locations[loc_key].id,
                    "star_rating": star_rating,
                    "price_per_night": price
                })
        
        # Krabi hotels
        for i, loc in enumerate(krabi_locations):
            loc_key = f"Krabi-{loc['name']}"
            # Add 2-3 hotels per location
            for j in range(random.randint(2, 3)):
                star_rating = random.randint(3, 5)
                price_base = {3: 40, 4: 90, 5: 180}[star_rating]
                price = price_base + random.randint(-15, 40)
                
                hotel_name = f"{['Andaman', 'Blue', 'Sea', 'Beach', 'Island', 'Tropical', 'Riverside', 'Cliff', 'Paradise'][random.randint(0, 8)]} {['Resort', 'Hotel', 'Lodge', 'Villa', 'Retreat', 'Bay Resort'][random.randint(0, 5)]}"
                
                hotels_data.append({
                    "name": hotel_name,
                    "description": f"A {star_rating}-star hotel located in {loc['name']}, offering comfortable accommodations with beautiful views.",
                    "location": loc["name"],
                    "location_id": db_locations[loc_key].id,
                    "star_rating": star_rating,
                    "price_per_night": price
                })
        
        # Add hotels to database
        db_hotels = []
        for hotel_data in hotels_data:
            hotel = models.Hotel(
                name=hotel_data["name"],
                description=hotel_data["description"],
                location=hotel_data["location"],
                location_id=hotel_data["location_id"],
                star_rating=hotel_data["star_rating"],
                price_per_night=hotel_data["price_per_night"]
            )
            db.add(hotel)
            db_hotels.append(hotel)
        
    db.commit()
    
        # Seed activities
        activities_data = []
        
        # Activity types
        activity_types = ["ADVENTURE", "CULTURAL", "RELAXATION", "NATURE", "NIGHTLIFE", "FAMILY", "ROMANTIC", "SHOPPING", "SIGHTSEEING", "FOOD"]
        
        # Phuket activities
        for i, loc in enumerate(phuket_locations):
            loc_key = f"Phuket-{loc['name']}"
            # Add 3-5 activities per location
            for j in range(random.randint(3, 5)):
                activity_type = activity_types[random.randint(0, len(activity_types)-1)]
                duration = random.uniform(1, 6)
                price = 20 + random.randint(0, 100)
                
                # Generate a realistic activity name
                activity_names = {
                    "ADVENTURE": ["Zip-lining Adventure", "ATV Tour", "White Water Rafting", "Scuba Diving", "Snorkeling Excursion", "Jet Ski Tour"],
                    "CULTURAL": ["Temple Tour", "Thai Cooking Class", "Traditional Dance Show", "Art Gallery Visit", "Local Craft Workshop"],
                    "RELAXATION": ["Spa Day", "Yoga on the Beach", "Sunset Cruise", "Hot Springs Bath", "Massage Treatment"],
                    "NATURE": ["Jungle Trek", "Bird Watching", "Elephant Sanctuary Visit", "Butterfly Garden", "Marine Life Tour"],
                    "NIGHTLIFE": ["Beach Club Party", "Bar Hopping Tour", "Cabaret Show", "Night Market Visit", "Rooftop Bar Experience"],
                    "FAMILY": ["Water Park Visit", "Aquarium Tour", "Mini Golf", "Zoo Visit", "Family Beach Day"],
                    "ROMANTIC": ["Private Beach Dinner", "Couple's Massage", "Sunset Sailing", "Honeymoon Photoshoot", "Candlelit Cave Dinner"],
                    "SHOPPING": ["Market Shopping Tour", "Mall Trip", "Souvenir Hunting", "Outlet Shopping", "Local Crafts Shopping"],
                    "SIGHTSEEING": ["Island Hopping", "City Tour", "Viewpoint Visit", "Historical Sites Tour", "Photography Tour"],
                    "FOOD": ["Street Food Tour", "Seafood Dinner", "Restaurant Hopping", "Food Market Visit", "Thai Dessert Tasting"]
                }
                
                activity_name = activity_names[activity_type][random.randint(0, len(activity_names[activity_type])-1)]
                
                activities_data.append({
                    "name": f"{activity_name} in {loc['name']}",
                    "description": f"Experience {activity_name.lower()} in the beautiful area of {loc['name']}. Perfect for {activity_type.lower()} enthusiasts.",
                    "location": loc["name"],
                    "location_id": db_locations[loc_key].id,
                    "type": activity_type,
                    "activity_type": activity_type,
                    "duration_hours": duration,
                    "duration_minutes": int(duration * 60),
                    "price": price
                })
        
        # Krabi activities
        for i, loc in enumerate(krabi_locations):
            loc_key = f"Krabi-{loc['name']}"
            # Add 3-5 activities per location
            for j in range(random.randint(3, 5)):
                activity_type = activity_types[random.randint(0, len(activity_types)-1)]
                duration = random.uniform(1, 6)
                price = 15 + random.randint(0, 90)
                
                # Generate a realistic activity name
                activity_names = {
                    "ADVENTURE": ["Rock Climbing", "Kayaking Tour", "Cave Exploration", "Cliff Jumping", "Deep Sea Fishing", "Paragliding"],
                    "CULTURAL": ["Local Village Visit", "Batik Painting Class", "Historical Tour", "Thai Language Class", "Traditional Crafts"],
                    "RELAXATION": ["Beach Yoga", "Sunset Boat Trip", "Island Retreat", "Natural Hot Springs", "Beachfront Massage"],
                    "NATURE": ["Mangrove Tour", "Wildlife Spotting", "National Park Visit", "Botanical Garden", "Birdwatching Tour"],
                    "NIGHTLIFE": ["Fire Show", "Beach Party", "Night Fishing", "Live Music Bar", "Moonlight Dinner"],
                    "FAMILY": ["Shell Collecting", "Snorkeling Lesson", "Pirate Ship Cruise", "Sand Castle Workshop", "Marine Education Tour"],
                    "ROMANTIC": ["Private Island Picnic", "Beachfront Villa Stay", "Love Boat Cruise", "Couple's Adventure", "Romantic Viewpoint Visit"],
                    "SHOPPING": ["Night Market Visit", "Handicraft Shopping", "Beachwear Boutiques", "Souvenir Hunting", "Art Shopping"],
                    "SIGHTSEEING": ["Four Islands Tour", "Emerald Pool Visit", "Hot Springs Tour", "Tiger Cave Temple", "Waterfall Exploration"],
                    "FOOD": ["Seafood BBQ", "Cooking on a Boat", "Floating Restaurant Visit", "Local Fruit Tasting", "Beachfront Dining"]
                }
                
                activity_name = activity_names[activity_type][random.randint(0, len(activity_names[activity_type])-1)]
                
                activities_data.append({
                    "name": f"{activity_name} in {loc['name']}",
                    "description": f"Experience {activity_name.lower()} in the beautiful area of {loc['name']}. Perfect for {activity_type.lower()} enthusiasts.",
                    "location": loc["name"],
                    "location_id": db_locations[loc_key].id,
                    "type": activity_type,
                    "activity_type": activity_type,
                    "duration_hours": duration,
                    "duration_minutes": int(duration * 60),
                    "price": price
                })
        
        # Add activities to database
        db_activities = []
        for activity_data in activities_data:
            activity = models.Activity(
                name=activity_data["name"],
                description=activity_data["description"],
                location=activity_data["location"],
                location_id=activity_data["location_id"],
                type=activity_data["type"],
                activity_type=activity_data["activity_type"],
                duration_hours=activity_data["duration_hours"],
                duration_minutes=activity_data["duration_minutes"],
                price=activity_data["price"]
            )
            db.add(activity)
            db_activities.append(activity)
        
    db.commit()
    
        # Create sample itineraries
        for region in ["Phuket", "Krabi"]:
            for nights in range(3, 9):  # 3-8 nights
                name = f"{nights}-Night {region} Adventure"
                description = f"Explore the beauty of {region} over {nights} nights. Experience the beaches, culture, and adventures this region has to offer."
                
                region_locations = phuket_locations if region == "Phuket" else krabi_locations
                region_location_keys = [f"{region}-{loc['name']}" for loc in region_locations]
                region_location_ids = [db_locations[key].id for key in region_location_keys]
                
                # Filter hotels and activities by region
                region_hotels = [hotel for hotel in db_hotels if hotel.location_id in region_location_ids]
                region_activities = [activity for activity in db_activities if activity.location_id in region_location_ids]
                
        total_price = 0
        
                # Create itinerary
                itinerary = models.Itinerary(
                    name=name,
                    description=description,
                    total_nights=nights,
                    region=region,
                    total_price=0,  # Will calculate later
                    best_season="November to April" if region == "Phuket" else "November to March",
                    avg_temperature="28-32°C" if region == "Phuket" else "27-31°C",
                    is_recommended=True
                )
                db.add(itinerary)
                db.flush()
                
                # Create days
                for day_num in range(1, nights + 1):
                    day = models.Day(
                        day_number=day_num,
                        itinerary_id=itinerary.id
                    )
                    db.add(day)
                    db.flush()
                    
                    # Add hotel
                    if region_hotels:
                        hotel = random.choice(region_hotels)
                        new_hotel = models.Hotel(
                            name=hotel.name,
                            description=hotel.description,
                            location=hotel.location,
                            location_id=hotel.location_id,
                            star_rating=hotel.star_rating,
                            price_per_night=hotel.price_per_night,
                            day_id=day.id
                        )
                        db.add(new_hotel)
                    total_price += hotel.price_per_night
            
                    # Add 2-3 activities
                    if region_activities:
                        day_activities = random.sample(region_activities, min(random.randint(2, 3), len(region_activities)))
                        for activity in day_activities:
                            new_activity = models.Activity(
                                name=activity.name,
                                description=activity.description,
                                location=activity.location,
                                location_id=activity.location_id,
                                type=activity.type,
                                activity_type=activity.activity_type,
                                duration_hours=activity.duration_hours,
                                duration_minutes=activity.duration_minutes,
                                price=activity.price,
                                day_id=day.id
                            )
                            db.add(new_activity)
                    total_price += activity.price
            
                    # Add transfer if not the last day
                    if day_num < nights:
                        from_location = random.choice(region_locations)["name"]
                        to_location = random.choice(region_locations)["name"]
                        
                        transport_types = ["CAR", "BOAT", "MINIVAN", "BUS"]
                        transport_type = random.choice(transport_types)
                        duration = random.uniform(0.5, 2.0)
                        transfer_price = 20 + random.uniform(10, 40)
                        
                        transfer = models.Transfer(
                            from_location=from_location,
                            to_location=to_location,
                            from_location_id=day_num,
                            to_location_id=day_num + 1,
                            transport_type=transport_type,
                            transportation_type=transport_type,
                            duration_hours=duration,
                            duration_minutes=int(duration * 60),
                            description=f"Transfer by {transport_type.lower()} from {from_location} to {to_location}",
                            price=transfer_price,
                            day_id=day.id
                        )
                        db.add(transfer)
                        total_price += transfer_price
                
                # Update total price
                itinerary.total_price = total_price
                db.commit()
        
        print(f"Database seeded successfully with {len(phuket_locations) + len(krabi_locations)} locations, {len(hotels_data)} hotels, {len(activities_data)} activities, and 12 itineraries.")
    
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {str(e)}")
        raise
    
    finally:
        db.close()

if __name__ == "__main__":
    # Create tables if they don't exist
    models.Base.metadata.create_all(bind=engine)
    
    # Seed the database
    seed_database()