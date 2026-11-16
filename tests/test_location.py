"""Unit tests for the geocoding helper (stdlib only, fake client)."""
import unittest

from location import geocode_location


class FakeClient:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error
        self.queries = []

    def geocode(self, location):
        self.queries.append(location)
        if self.error:
            raise self.error
        return self.result


class GeocodeLocationTests(unittest.TestCase):
    def test_success_returns_coordinates_and_no_message(self):
        client = FakeClient([{"geometry": {"location": {"lat": 48.85, "lng": 2.35}}}])
        coords, message = geocode_location(client, "Paris")
        self.assertEqual(coords, {"lat": 48.85, "lng": 2.35})
        self.assertIsNone(message)
        self.assertEqual(client.queries, ["Paris"])

    def test_empty_result_gets_location_specific_message(self):
        coords, message = geocode_location(FakeClient([]), "Nowhere")
        self.assertIsNone(coords)
        self.assertIn("Could not find 'Nowhere'", message)
        self.assertIn("more specific city", message)

    def test_api_error_is_reported_separately(self):
        coords, message = geocode_location(FakeClient(error=RuntimeError("quota")), "Paris")
        self.assertIsNone(coords)
        self.assertIn("Error geocoding Paris", message)
        self.assertIn("billing", message)
        self.assertNotIn("Could not find", message)


if __name__ == "__main__":
    unittest.main()
