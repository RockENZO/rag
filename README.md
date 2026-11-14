# Restaurant Recommendation RAG System

This project is a Retrieval-Augmented Generation (RAG) system for restaurant recommendations, leveraging LlamaIndex, Google Maps Platform, and Groq.

## Features

- Accepts any user-specified city for restaurant searches.
- Fetches top 10 restaurants near the location using Google Maps Places API.
- Uses Groq LLM to generate personalized recommendations based on retrieved data.

## Setup

Install dependencies from the repository root.

```sh
python -m pip install -r requirements.txt
```

Provide `GROQ_API_KEY` and `GOOGLE_MAPS_API_KEY` through your shell environment or secret manager. Keep keys out of source files and commits.

The Google Cloud project must have billing enabled and access to both the [Geocoding API](https://developers.google.com/maps/documentation/geocoding/usage-and-billing) and [Places API (Legacy)](https://developers.google.com/maps/documentation/places/web-service/legacy/overview-legacy). The app calls Nearby Search (Legacy). New Google Cloud projects cannot enable Places API (Legacy), so running this version requires an existing project with access. Google Maps requests can incur charges.

## Usage

```sh
python src/main.py
```

Enter queries like "restaurants near Paris" for recommendations.

## Architecture

- **Retrieval**: Google Maps API fetches real-time restaurant data.
- **Augmentation**: Data is passed to the LLM for context.
- **Generation**: LLM produces natural, personalized responses.