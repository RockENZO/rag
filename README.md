# Restaurant Recommendation RAG System

This project is a Retrieval-Augmented Generation (RAG) system for restaurant recommendations, leveraging LangChain, LlamaIndex, Google Maps Platform API, and Groq API.

## Features

- Accepts any user-specified city for restaurant searches.
- Fetches top 10 restaurants near the location using Google Maps Places API.
- Uses Groq LLM to generate personalized recommendations based on retrieved data.

## Setup

1. Install dependencies:
   pip install -r requirements.txt

2. Set up API keys (or use hardcoded for testing):
   - GROQ_API_KEY
   - GOOGLE_MAPS_API_KEY (ensure Places API is enabled)

## Usage

Run the main script:
python src/main.py

Enter queries like "restaurants near Paris" for recommendations.

## Architecture

- **Retrieval**: Google Maps API fetches real-time restaurant data.
- **Augmentation**: Data is passed to the LLM for context.
- **Generation**: LLM produces natural, personalized responses.