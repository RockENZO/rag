import os
from langchain_groq import ChatGroq
from llama_index.llms.groq import Groq
from googlemaps import Client as GoogleMapsClient

# Set up API keys
groq_api_key = ''
google_maps_api_key = ''

if not groq_api_key or not google_maps_api_key:
    print("Please set GROQ_API_KEY and GOOGLE_MAPS_API_KEY environment variables.")
    exit(1)

# Initialize clients
llm = Groq(api_key=groq_api_key, model="llama-3.1-8b-instant")
gmaps = GoogleMapsClient(key=google_maps_api_key)

# Interactive restaurant recommendation RAG
while True:
    user_query = input("Enter your restaurant query (e.g., 'restaurants near Paris') or 'quit' to exit: ")
    if user_query.lower() == 'quit':
        break
    
    if 'restaurant' in user_query.lower() and ('near' in user_query.lower() or 'in' in user_query.lower()):
        # Extract location from query
        query_lower = user_query.lower()
        location_str = None
        if 'near' in query_lower:
            parts = query_lower.split('near')
            if len(parts) > 1:
                location_str = parts[1].strip().title()  # Capitalize for geocoding
        elif 'in' in query_lower:
            parts = query_lower.split('in')
            if len(parts) > 1:
                location_str = parts[1].strip().title()
        
        if not location_str:
            print("Please specify a location, e.g., 'restaurants near Paris'.")
            continue
        
        # Geocode to get lat/lng
        geocode_result = gmaps.geocode(location_str)
        if geocode_result:
            lat = geocode_result[0]['geometry']['location']['lat']
            lng = geocode_result[0]['geometry']['location']['lng']
            try:
                # Use Google Maps Places API for nearby restaurants
                places_result = gmaps.places_nearby(location=(lat, lng), radius=5000, type='restaurant')
                restaurants = places_result.get('results', [])[:10]  # Top 10
                
                if restaurants:
                    # Prepare data for LLM (RAG-style augmentation)
                    restaurant_info = "\n".join([f"- {r['name']}: Rating {r.get('rating', 'N/A')}, Address: {r.get('vicinity', 'N/A')}, Price Level: {r.get('price_level', 'N/A')}" for r in restaurants])
                    llm_prompt = f"Based on the following restaurant data near {location_str}, provide personalized recommendations with brief descriptions:\n{restaurant_info}\n\nUser query: {user_query}"
                    summary = llm.complete(llm_prompt)
                    print("Restaurant Recommendations:", summary)
                else:
                    print("No restaurants found near that location.")
            except Exception as e:
                print(f"Error fetching restaurants: {e}. Ensure Places API is enabled for your Google Maps key.")
        else:
            print("Could not geocode the location.")
    else:
        print("This system specializes in restaurant recommendations. Please ask about restaurants near a location.")