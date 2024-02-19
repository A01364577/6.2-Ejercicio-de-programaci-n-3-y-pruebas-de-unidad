"""
Unit tests for the Reservation class.
"""

import unittest
import json
from A01364577_A6_2 import Reservation


class TestReservation(unittest.TestCase):
    """
    Test cases for the Reservation class.
    """

    def setUp(self):
        """
        Set up a test reservation object.
        """
        self.test_reservation = Reservation("John Doe", "Test Hotel", "Single", "2024-02-20", "2024-02-25")

    def test_create_reservation(self):
        """
        Test creating a reservation.
        """
        # Ensure the reservation is not already in the file
        self.assertFalse(self._reservation_exists(self.test_reservation.to_json()))

        # Create the reservation
        self.test_reservation.create_reservation()

        # Check if the reservation is now in the file
        self.assertTrue(self._reservation_exists(self.test_reservation.to_json()))

    def test_cancel_reservation(self):
        """
        Test canceling a reservation.
        """
        # Create the reservation
        self.test_reservation.create_reservation()

        # Ensure the reservation exists
        self.assertTrue(self._reservation_exists(self.test_reservation.to_json()))

        # Cancel the reservation
        self.test_reservation.cancel_reservation()

        # Ensure the reservation no longer exists
        self.assertFalse(self._reservation_exists(self.test_reservation.to_json()))

    def _reservation_exists(self, reservation_data):
        """
        Check if a reservation exists in the reservations file.
        """
        try:
            with open("reservations.json", 'r', encoding='utf-8') as f:
                reservations = json.load(f)
                return reservation_data in reservations
        except FileNotFoundError:
            return False


if __name__ == '__main__':
    unittest.main()
