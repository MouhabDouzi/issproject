# services/ai_service.py
import os
import json
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = None
try:
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Warning: OPENAI_API_KEY not found in environment variables")
    else:
        # Initialize the client with just the API key
        client = OpenAI(api_key=api_key)
except Exception as e:
    print(f"Error initializing OpenAI client: {str(e)}")
    client = None

class TravelRecommender:
    def __init__(self):
        self.destinations_data = self._load_destinations_data()
        
    def _load_destinations_data(self):
        # This would typically load from a database or API
        return {
            "destinations": [
                {
                    "name": "Bangkok, Thailand",
                    "budget_level": "low",
                    "temperature": "hot",
                    "popular_seasons": ["spring", "summer"],
                    "attractions": ["temples", "street food", "markets"],
                    "avg_daily_cost": 50
                },
                {
                    "name": "Paris, France",
                    "budget_level": "high",
                    "temperature": "mild",
                    "popular_seasons": ["spring", "fall"],
                    "attractions": ["museums", "architecture", "cuisine"],
                    "avg_daily_cost": 150
                },
                {
                    "name": "Tokyo, Japan",
                    "budget_level": "medium",
                    "temperature": "mild",
                    "popular_seasons": ["spring", "fall"],
                    "attractions": ["technology", "culture", "food"],
                    "avg_daily_cost": 100
                },
                {
                    "name": "New York, USA",
                    "budget_level": "high",
                    "temperature": "cold",
                    "popular_seasons": ["spring", "fall"],
                    "attractions": ["museums", "shopping", "entertainment"],
                    "avg_daily_cost": 200
                },
                {
                    "name": "Barcelona, Spain",
                    "budget_level": "medium",
                    "temperature": "hot",
                    "popular_seasons": ["summer", "spring"],
                    "attractions": ["architecture", "beaches", "food"],
                    "avg_daily_cost": 80
                }
            ]
        }
    
    def generate_destination(self, budget, temperature, purpose, duration):
        if client:
            try:
                # Use OpenAI for sophisticated recommendations
                prompt = f"""
                Based on the following criteria, suggest a travel destination:
                - Budget: {budget}
                - Temperature preference: {temperature}
                - Purpose: {purpose}
                - Duration: {duration}
                
                Provide a detailed response with:
                1. Best matching destination
                2. Brief explanation
                3. Key attractions
                4. Estimated daily budget
                5. Best time to visit
                6. Local customs to be aware of
                7. Safety tips
                
                Format your response as a JSON object with these keys: destination, explanation, attractions, daily_budget, best_time, customs, safety_tips
                """
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a travel expert providing personalized destination recommendations."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                content = response.choices[0].message.content
                if content:
                    try:
                        return json.loads(content)
                    except json.JSONDecodeError:
                        # If the response is not valid JSON, return it as a string
                        return {"recommendation": content}
                return self._fallback_destination_recommendation(budget, temperature)
                
            except Exception as e:
                print(f"OpenAI API error: {e}")
                return self._fallback_destination_recommendation(budget, temperature)
        else:
            # Fallback to rule-based system if API fails or not available
            return self._fallback_destination_recommendation(budget, temperature)
    
    def _fallback_destination_recommendation(self, budget, temperature):
        """Provide a basic destination recommendation when OpenAI API is not available"""
        # Simple recommendation logic based on budget and temperature
        if budget == 'Low':
            if temperature == 'Hot':
                return {
                    "destination": "Tunisia",
                    "explanation": "Tunisia offers affordable travel options with warm weather.",
                    "best_time": "Spring or Fall",
                    "customs": "Respect local customs and dress modestly.",
                    "safety": "Generally safe, but be cautious in tourist areas."
                }
            elif temperature == 'Mild':
                return {
                    "destination": "Morocco",
                    "explanation": "Morocco provides budget-friendly options with mild weather.",
                    "best_time": "Spring or Fall",
                    "customs": "Respect local customs and dress modestly.",
                    "safety": "Generally safe, but be cautious in tourist areas."
                }
            else:  # Cold
                return {
                    "destination": "Romania",
                    "explanation": "Romania offers affordable travel with cooler temperatures.",
                    "best_time": "Summer",
                    "customs": "Standard European customs apply.",
                    "safety": "Generally safe for travelers."
                }
        elif budget == 'Medium':
            if temperature == 'Hot':
                return {
                    "destination": "Spain",
                    "explanation": "Spain offers a good balance of cost and warm weather.",
                    "best_time": "Spring or Fall",
                    "customs": "Standard European customs apply.",
                    "safety": "Generally safe for travelers."
                }
            elif temperature == 'Mild':
                return {
                    "destination": "Portugal",
                    "explanation": "Portugal provides moderate costs with mild weather.",
                    "best_time": "Spring or Fall",
                    "customs": "Standard European customs apply.",
                    "safety": "Generally safe for travelers."
                }
            else:  # Cold
                return {
                    "destination": "Ireland",
                    "explanation": "Ireland offers moderate costs with cooler temperatures.",
                    "best_time": "Summer",
                    "customs": "Standard European customs apply.",
                    "safety": "Generally safe for travelers."
                }
        else:  # High budget
            if temperature == 'Hot':
                return {
                    "destination": "Greece",
                    "explanation": "Greece offers luxury options with warm weather.",
                    "best_time": "Spring or Fall",
                    "customs": "Standard European customs apply.",
                    "safety": "Generally safe for travelers."
                }
            elif temperature == 'Mild':
                return {
                    "destination": "Italy",
                    "explanation": "Italy provides luxury options with mild weather.",
                    "best_time": "Spring or Fall",
                    "customs": "Standard European customs apply.",
                    "safety": "Generally safe for travelers."
                }
            else:  # Cold
                return {
                    "destination": "Switzerland",
                    "explanation": "Switzerland offers luxury options with cooler temperatures.",
                    "best_time": "Summer",
                    "customs": "Standard European customs apply.",
                    "safety": "Generally safe for travelers."
                }

    def generate_itinerary(self, destination, duration, budget, purpose, travelers, preferences):
        if client:
            try:
                # Use OpenAI for personalized itinerary generation
                prompt = f"""
                Create a detailed travel itinerary for:
                Destination: {destination}
                Duration: {duration}
                Budget: {budget}
                Purpose: {purpose}
                Number of travelers: {travelers}
                Preferences: {preferences}
                
                Include:
                1. Day-by-day schedule with specific times
                2. Recommended activities with descriptions
                3. Local cuisine suggestions with restaurant types
                4. Transportation tips between locations
                5. Budget considerations with cost estimates
                6. Cultural experiences and local events
                7. Photo opportunities and scenic spots
                8. Alternative options in case of bad weather
                
                Format your response as a JSON object with these keys: destination, duration, budget, purpose, days (array of day objects), cuisine, transportation, budget_breakdown, cultural_experiences, photo_spots, alternatives
                """
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a travel planner creating detailed, personalized itineraries."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                content = response.choices[0].message.content
                if content:
                    try:
                        return json.loads(content)
                    except json.JSONDecodeError:
                        # If the response is not valid JSON, return it as a string
                        return {"itinerary": content}
                return self._generate_template_itinerary(destination, duration, purpose)
                
            except Exception as e:
                print(f"OpenAI API error: {e}")
                return self._generate_template_itinerary(destination, duration, purpose)
        else:
            # Fallback to template-based itinerary
            return self._generate_template_itinerary(destination, duration, purpose)
    
    def _generate_template_itinerary(self, destination, duration, purpose):
        """Generate a basic template itinerary when OpenAI API is not available"""
        # Convert duration string to number of days
        days_count = 7  # Default
        if 'days' in duration:
            try:
                days_count = int(duration.split()[0])
            except:
                pass
        
        # Generate days based on purpose
        days = []
        for i in range(days_count):
            day_num = i + 1
            if purpose == 'Leisure':
                days.append({
                    "day": day_num,
                    "morning": f"Breakfast at hotel, then visit {destination} city center",
                    "afternoon": f"Lunch at a local restaurant, then explore {destination} attractions",
                    "evening": f"Dinner at a recommended restaurant, then evening entertainment"
                })
            elif purpose == 'Adventure':
                days.append({
                    "day": day_num,
                    "morning": f"Early breakfast, then outdoor adventure activity in {destination}",
                    "afternoon": f"Lunch on the go, then continue adventure activities",
                    "evening": f"Dinner at a local restaurant, then relaxation"
                })
            elif purpose == 'Cultural':
                days.append({
                    "day": day_num,
                    "morning": f"Breakfast at hotel, then visit cultural sites in {destination}",
                    "afternoon": f"Lunch at a local restaurant, then continue cultural exploration",
                    "evening": f"Dinner at a traditional restaurant, then cultural performance"
                })
            elif purpose == 'Business':
                days.append({
                    "day": day_num,
                    "morning": f"Breakfast at hotel, then business meetings in {destination}",
                    "afternoon": f"Lunch meeting, then continue business activities",
                    "evening": f"Dinner meeting or networking event"
                })
            else:  # Default
                days.append({
                    "day": day_num,
                    "morning": f"Breakfast at hotel, then explore {destination}",
                    "afternoon": f"Lunch at a local restaurant, then continue exploration",
                    "evening": f"Dinner at a recommended restaurant, then evening activities"
                })
        
        return {
            "days": days,
            "costs": {
                "Accommodation": "$100-200 per night",
                "Food": "$30-50 per day",
                "Activities": "$20-40 per day",
                "Transportation": "$10-30 per day"
            },
            "transportation": "Public transit, taxis, or rental car recommended",
            "food": "Local restaurants and cafes recommended",
            "cultural_experiences": [
                f"Visit local markets in {destination}",
                f"Experience local festivals in {destination}",
                f"Learn about local history in {destination}"
            ],
            "photo_spots": [
                f"City center of {destination}",
                f"Local landmarks in {destination}",
                f"Scenic viewpoints in {destination}"
            ],
            "alternatives": [
                f"Indoor museums in {destination}",
                f"Shopping centers in {destination}",
                f"Cafes and restaurants in {destination}"
            ],
            "packing_list": [
                "Comfortable walking shoes",
                "Weather-appropriate clothing",
                "Camera or smartphone",
                "Travel documents",
                "Basic first aid kit"
            ],
            "health_safety": [
                f"Check travel advisories for {destination}",
                "Keep valuables secure",
                "Stay hydrated",
                "Follow local health guidelines"
            ]
        }

# Initialize the recommender
travel_recommender = TravelRecommender()

# Export functions
def generate_destination(budget, temperature, purpose, duration):
    """Generate a destination recommendation based on user preferences"""
    try:
        # Create a prompt for the OpenAI API
        prompt = f"""
        Recommend a travel destination based on the following preferences:
        - Budget: {budget}
        - Temperature: {temperature}
        - Purpose: {purpose}
        - Duration: {duration}
        
        Please provide a detailed recommendation with:
        1. The recommended destination
        2. Why it's a good fit for these preferences
        3. Best time to visit
        4. Local customs and etiquette
        5. Safety considerations
        
        Format your response as a JSON object with these keys: destination, explanation, best_time, customs, safety
        """
        
        # Call OpenAI API
        content = _call_openai_api(prompt)
        
        if content:
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # If the response is not valid JSON, return it as a string
                return {"destination": content}
        
        # Fallback to basic recommendation
        return _fallback_destination_recommendation(budget, temperature)
    except Exception as e:
        print(f"Error generating destination: {str(e)}")
        # Fallback to basic recommendation
        return _fallback_destination_recommendation(budget, temperature)

def generate_itinerary(destination, duration, budget, purpose, travelers, preferences):
    """Generate a detailed itinerary based on destination and preferences"""
    try:
        # Create a prompt for the OpenAI API
        prompt = f"""
        Create a detailed travel itinerary for {destination} with the following preferences:
        - Duration: {duration}
        - Budget: {budget}
        - Purpose: {purpose}
        - Number of travelers: {travelers}
        - Additional preferences: {preferences}
        
        Please provide a comprehensive itinerary with:
        1. Day-by-day schedule with specific times and activities
        2. Estimated costs for each day
        3. Transportation recommendations
        4. Restaurant and food recommendations
        5. Cultural experiences to try
        6. Photo opportunities
        7. Alternative plans in case of bad weather
        8. Packing list recommendations
        9. Health and safety considerations
        
        Format your response as a JSON object with these keys: days, costs, transportation, food, cultural_experiences, photo_spots, alternatives, packing_list, health_safety
        """
        
        # Call OpenAI API
        content = _call_openai_api(prompt)
        
        if content:
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # If the response is not valid JSON, return it as a string
                return {"days": [{"day": 1, "morning": content, "afternoon": "", "evening": ""}]}
        
        # Fallback to template itinerary
        return _generate_template_itinerary(destination, duration, purpose)
    except Exception as e:
        print(f"Error generating itinerary: {str(e)}")
        # Fallback to template itinerary
        return _generate_template_itinerary(destination, duration, purpose)

def generate_travel_plan(preferences):
    """Generate a complete travel plan based on user preferences"""
    try:
        # Extract preferences
        budget = preferences.get('budget', 'Medium')
        temperature = preferences.get('temperature', 'Mild')
        purpose = preferences.get('purpose', 'Leisure')
        duration = preferences.get('duration', '7 days')
        travelers = preferences.get('travelers', 1)
        additional = preferences.get('additional', '')
        
        # Generate destination
        destination = generate_destination(budget, temperature, purpose, duration)
        
        # Generate itinerary
        itinerary = generate_itinerary(destination, duration, budget, purpose, travelers, additional)
        
        return {
            'destination': destination,
            'itinerary': itinerary
        }
    except Exception as e:
        print(f"Error generating travel plan: {str(e)}")
        return {
            'destination': 'Error generating destination',
            'itinerary': {
                'days': []
            }
        }

# Update the OpenAI API calls to handle client being None
def _call_openai_api(prompt, model="gpt-3.5-turbo"):
    """Helper function to call OpenAI API with error handling"""
    if not client:
        return None
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful travel assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {str(e)}")
        return None

def _fallback_destination_recommendation(budget, temperature):
    """Provide a basic destination recommendation when OpenAI API is not available"""
    # Simple recommendation logic based on budget and temperature
    if budget == 'Low':
        if temperature == 'Hot':
            return {
                "destination": "Tunisia",
                "explanation": "Tunisia offers affordable travel options with warm weather.",
                "best_time": "Spring or Fall",
                "customs": "Respect local customs and dress modestly.",
                "safety": "Generally safe, but be cautious in tourist areas."
            }
        elif temperature == 'Mild':
            return {
                "destination": "Morocco",
                "explanation": "Morocco provides budget-friendly options with mild weather.",
                "best_time": "Spring or Fall",
                "customs": "Respect local customs and dress modestly.",
                "safety": "Generally safe, but be cautious in tourist areas."
            }
        else:  # Cold
            return {
                "destination": "Romania",
                "explanation": "Romania offers affordable travel with cooler temperatures.",
                "best_time": "Summer",
                "customs": "Standard European customs apply.",
                "safety": "Generally safe for travelers."
            }
    elif budget == 'Medium':
        if temperature == 'Hot':
            return {
                "destination": "Spain",
                "explanation": "Spain offers a good balance of cost and warm weather.",
                "best_time": "Spring or Fall",
                "customs": "Standard European customs apply.",
                "safety": "Generally safe for travelers."
            }
        elif temperature == 'Mild':
            return {
                "destination": "Portugal",
                "explanation": "Portugal provides moderate costs with mild weather.",
                "best_time": "Spring or Fall",
                "customs": "Standard European customs apply.",
                "safety": "Generally safe for travelers."
            }
        else:  # Cold
            return {
                "destination": "Ireland",
                "explanation": "Ireland offers moderate costs with cooler temperatures.",
                "best_time": "Summer",
                "customs": "Standard European customs apply.",
                "safety": "Generally safe for travelers."
            }
    else:  # High budget
        if temperature == 'Hot':
            return {
                "destination": "Greece",
                "explanation": "Greece offers luxury options with warm weather.",
                "best_time": "Spring or Fall",
                "customs": "Standard European customs apply.",
                "safety": "Generally safe for travelers."
            }
        elif temperature == 'Mild':
            return {
                "destination": "Italy",
                "explanation": "Italy provides luxury options with mild weather.",
                "best_time": "Spring or Fall",
                "customs": "Standard European customs apply.",
                "safety": "Generally safe for travelers."
            }
        else:  # Cold
            return {
                "destination": "Switzerland",
                "explanation": "Switzerland offers luxury options with cooler temperatures.",
                "best_time": "Summer",
                "customs": "Standard European customs apply.",
                "safety": "Generally safe for travelers."
            }

def _generate_template_itinerary(destination, duration, purpose):
    """Generate a basic template itinerary when OpenAI API is not available"""
    # Convert duration string to number of days
    days_count = 7  # Default
    if 'days' in duration:
        try:
            days_count = int(duration.split()[0])
        except:
            pass
    
    # Generate days based on purpose
    days = []
    for i in range(days_count):
        day_num = i + 1
        if purpose == 'Leisure':
            days.append({
                "day": day_num,
                "morning": f"Breakfast at hotel, then visit {destination} city center",
                "afternoon": f"Lunch at a local restaurant, then explore {destination} attractions",
                "evening": f"Dinner at a recommended restaurant, then evening entertainment"
            })
        elif purpose == 'Adventure':
            days.append({
                "day": day_num,
                "morning": f"Early breakfast, then outdoor adventure activity in {destination}",
                "afternoon": f"Lunch on the go, then continue adventure activities",
                "evening": f"Dinner at a local restaurant, then relaxation"
            })
        elif purpose == 'Cultural':
            days.append({
                "day": day_num,
                "morning": f"Breakfast at hotel, then visit cultural sites in {destination}",
                "afternoon": f"Lunch at a local restaurant, then continue cultural exploration",
                "evening": f"Dinner at a traditional restaurant, then cultural performance"
            })
        elif purpose == 'Business':
            days.append({
                "day": day_num,
                "morning": f"Breakfast at hotel, then business meetings in {destination}",
                "afternoon": f"Lunch meeting, then continue business activities",
                "evening": f"Dinner meeting or networking event"
            })
        else:  # Default
            days.append({
                "day": day_num,
                "morning": f"Breakfast at hotel, then explore {destination}",
                "afternoon": f"Lunch at a local restaurant, then continue exploration",
                "evening": f"Dinner at a recommended restaurant, then evening activities"
            })
    
    return {
        "days": days,
        "costs": {
            "Accommodation": "$100-200 per night",
            "Food": "$30-50 per day",
            "Activities": "$20-40 per day",
            "Transportation": "$10-30 per day"
        },
        "transportation": "Public transit, taxis, or rental car recommended",
        "food": "Local restaurants and cafes recommended",
        "cultural_experiences": [
            f"Visit local markets in {destination}",
            f"Experience local festivals in {destination}",
            f"Learn about local history in {destination}"
        ],
        "photo_spots": [
            f"City center of {destination}",
            f"Local landmarks in {destination}",
            f"Scenic viewpoints in {destination}"
        ],
        "alternatives": [
            f"Indoor museums in {destination}",
            f"Shopping centers in {destination}",
            f"Cafes and restaurants in {destination}"
        ],
        "packing_list": [
            "Comfortable walking shoes",
            "Weather-appropriate clothing",
            "Camera or smartphone",
            "Travel documents",
            "Basic first aid kit"
        ],
        "health_safety": [
            f"Check travel advisories for {destination}",
            "Keep valuables secure",
            "Stay hydrated",
            "Follow local health guidelines"
        ]
    }