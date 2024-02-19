"""
Unit tests for the Hotel class.
"""

import unittest
import json
import sys
from io import StringIO
from A01364577_A6_2 import Hotel


class TestHotel(unittest.TestCase):
    """
    Test cases for the Hotel class.
    """

    def setUp(self):
        """
        Set up a temporary test file for hotels.
        """
        with open("test_hotels.json", "w") as f:
            json.dump([], f)

    def tearDown(self):
        """
        Remove the temporary test file after each test.
        """
        import os
        os.remove("hotels.json")

    def test_create_hotel(self):
        """
        Test creating a hotel.
        """
        # Create a test hotel
        test_hotel = Hotel("Test Hotel", "Test Location")

        # Create the hotel using the create_hotel method
        test_hotel.create_hotel()

        # Load hotels data from file
        with open("hotels.json", 'r', encoding='utf-8') as f:
            hotels_data = json.load(f)

        # Check if the hotel is created successfully
        self.assertTrue(any(hotel['name'] == "Test Hotel" for hotel in hotels_data))

    def test_delete_hotel(self):
        """
        Test deleting a hotel.
        """
        # Create a test hotel
        test_hotel = Hotel("Test Hotel", "Test Location")

        # Create the hotel using the create_hotel method
        test_hotel.create_hotel()

        # Delete the hotel using the delete_hotel method
        test_hotel.delete_hotel("Test Hotel")

        # Load hotels data from file
        with open("hotels.json", 'r', encoding='utf-8') as f:
            hotels_data = json.load(f)

        # Check if the hotel is deleted successfully
        self.assertFalse(any(hotel['name'] == "Test Hotel" for hotel in hotels_data))

    def test_display_hotel_info(self):
        """
        Test displaying hotel information.
        """
        # Create a test hotel
        test_hotel = Hotel("Test Hotel", "Test Location")
        test_hotel.create_hotel()

        # Redirect stdout to capture print output
        captured_output = StringIO()
        sys.stdout = captured_output

        # Call display_hotel_info method
        test_hotel.display_hotel_info()

        # Reset redirection of stdout
        sys.stdout = sys.__stdout__

        # Get the printed output
        printed_output = captured_output.getvalue().strip()

        # Check if the displayed information matches the expected output
        expected_output = """Hotel Name: Test Hotel
Location: Test Location
Rooms: None
Reservations: 0"""

        self.assertEqual(printed_output, expected_output)

    def test_modify_hotel_info(self):
        """
        Test modifying hotel information.
        """
        # Create a test hotel
        test_hotel = Hotel("Test Hotel", "Test Location")

        # Create the hotel using the create_hotel method
        test_hotel.create_hotel()

        # Modify the hotel information using the modify_hotel_info method
        test_hotel.modify_hotel_info("New Test Hotel", "New Test Location")

        # Load hotels data from file
        with open("hotels.json", 'r', encoding='utf-8') as f:
            hotels_data = json.load(f)

        # Check if the hotel information is modified successfully
        modified_hotel = next((hotel for hotel in hotels_data if hotel['name'] == "New Test Hotel"), None)
        self.assertIsNotNone(modified_hotel)
        self.assertEqual(modified_hotel['location'], "New Test Location")


if __name__ == '__main__':
    unittest.main()
