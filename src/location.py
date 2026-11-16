"""Geocoding helper kept separate from the interactive demo for testability."""


def geocode_location(gmaps, location):
    """Return ``((lat, lng), None)`` or ``(None, user_message)``.

    Network/API/billing failures are reported differently from an empty
    geocode result so the caller can give an actionable message.
    """
    try:
        results = gmaps.geocode(location)
    except Exception as exc:  # noqa: BLE001 - the demo must keep running
        return None, (
            f"Error geocoding {location}: {exc}. Check network access, billing "
            "and Geocoding API enablement."
        )
    if not results:
        return None, (
            f"Could not find '{location}'. Try a more specific city name, or add the country."
        )
    return results[0]["geometry"]["location"], None
