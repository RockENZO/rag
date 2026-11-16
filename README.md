# Restaurant Recommendation RAG System

This project is a Retrieval-Augmented Generation (RAG) system for restaurant recommendations, leveraging LlamaIndex, Google Maps Platform, and Groq.

## Features

- Accepts any user-specified city for restaurant searches.
- Fetches top 10 restaurants near the location using Google Maps Places API.
- Uses Groq LLM to generate personalized recommendations based on retrieved data.

## Scope and limitations

This is a small learning/demo project, not a production restaurant recommender. It retrieves one page of roughly 10 nearby restaurants and indexes those records; for data this small, passing the same rows directly in the prompt would likely be simpler and cheaper, and the vector index is mainly here to demonstrate a RAG pipeline. Recommendations depend on Google Maps data, the model's interpretation and the extracted location, so they can be incomplete or wrong. There is no accuracy benchmark or automated test suite.

The small geocoding helper is covered by stdlib unit tests. No API key is needed for them:

```sh
PYTHONPATH=src python -m unittest discover -s tests -v
```

CI runs the same command on Python 3.10 and 3.12. The full app still needs live Google/Groq credentials and is not exercised by those tests.

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