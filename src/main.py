import os
from llama_index.core import VectorStoreIndex, Document, PromptTemplate
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.llms.groq import Groq
from googlemaps import Client as GoogleMapsClient

from location import geocode_location

# Disable tokenizers parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Set up API keys
groq_api_key = os.getenv('GROQ_API_KEY', '')
google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY', '')

if not groq_api_key or not google_maps_api_key:
    print("Please set GROQ_API_KEY and GOOGLE_MAPS_API_KEY environment variables.")
    exit(1)

# Initialize clients
gmaps = GoogleMapsClient(key=google_maps_api_key)
embed_model = FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5")
llm = Groq(api_key=groq_api_key, model="llama-3.1-8b-instant")

# Custom prompt for RAG
qa_prompt_tmpl = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, "
    "answer the query: {query_str}\n"
    "Provide specific restaurant recommendations with names, ratings, addresses, and brief descriptions.\n"
)
qa_prompt = PromptTemplate(qa_prompt_tmpl)

# Interactive restaurant recommendation RAG
while True:
    user_query = input("Enter your restaurant query (e.g., 'restaurants near Paris') or 'quit' to exit: ")
    if user_query.lower() == 'quit':
        break
    
    # Use LLM to extract location from query
    location_prompt = f"Extract the city or location name from this query. If no location is mentioned, respond with 'none'. Query: '{user_query}'"
    location_response = llm.complete(location_prompt).text.strip().lower()
    
    if location_response == 'none' or not location_response:
        print("Please specify a location in your query, e.g., 'restaurants near Paris'.")
        continue
    
    location_str = location_response.title()  # Capitalize for geocoding
    
    # Geocode to get lat/lng. The helper separates API failures from an empty
    # result so each gets an actionable message.
    coords, message = geocode_location(gmaps, location_str)
    if message:
        print(message)
        continue

    lat = coords["lat"]
    lng = coords["lng"]
    try:
        # Use Google Maps Places API for nearby restaurants
        places_result = gmaps.places_nearby(location=(lat, lng), radius=5000, type='restaurant')
        restaurants = places_result.get('results', [])[:10]  # Top 10

        if restaurants:
            # Create LlamaIndex documents for RAG
            documents = []
            for r in restaurants:
                text = f"Name: {r['name']}, Rating: {r.get('rating', 'N/A')}, Address: {r.get('vicinity', 'N/A')}, Price Level: {r.get('price_level', 'N/A')}"
                documents.append(Document(text=text))

            # Build vector index with LlamaIndex
            index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)

            # Create query engine with LlamaIndex
            query_engine = index.as_query_engine(llm=llm, text_qa_template=qa_prompt)

            # Run the RAG query
            response = query_engine.query(user_query)
            print("Restaurant Recommendations:", response)
        else:
            print("No restaurants found near that location.")
    except Exception as e:
        print(f"Error fetching restaurants: {e}. Ensure Places API is enabled for your Google Maps key.")
