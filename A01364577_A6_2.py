"""
Module implementing hotel reservation system.
"""

import json
from datetime import datetime


class Hotel:
    """
    Represents a hotel.
    """

    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.rooms = []
        self.reservations = []

    def create_hotel(self):
        """
        Create a new hotel.
        """
        hotels = self._load_hotels()
        hotels.append(self.__dict__)
        self._save_hotels(hotels)

    def delete_hotel(self, hotel_name):
        """
        Delete a hotel.
        """
        hotels = self._load_hotels()
        hotels = [h for h in hotels if h['name'] != hotel_name]
        self._save_hotels(hotels)

    def display_hotel_info(self):
        """
        Display information about a hotel.
        """
        hotels = self._load_hotels()
        for hotel in hotels:
            if hotel['name'] == self.name:
                print("Hotel Name:", hotel['name'])
                print("Location:", hotel['location'])
                print("Rooms:" if hotel['rooms'] else "Rooms: None")
                print("Reservations:", len(hotel['reservations']))
                break
        else:
            print("Hotel not found.")

    def modify_hotel_info(self, new_name, new_location):
        """
        Modify hotel information.
        """
        hotels = self._load_hotels()
        for hotel in hotels:
            if hotel['name'] == self.name:
                hotel['name'] = new_name
                hotel['location'] = new_location
                break
        self._save_hotels(hotels)

    def _load_hotels(self, file_name="hotels.json"):
        """
        Load hotel data from a JSON file.
        """
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                hotels = json.load(f)
        except FileNotFoundError:
            hotels = []
        return hotels

    def _save_hotels(self, hotels):
        """
        Save hotel data to a JSON file.
        """
        with open("hotels.json", 'w', encoding='utf-8') as f:
            json.dump(hotels, f, indent=4)


class Customer:
    """
    Represents a customer.
    """

    def __init__(self, customer_name, hotel_name, room_type, check_in, check_out):
        self.customer_name = customer_name
        self.hotel_name = hotel_name
        self.room_type = room_type
        self.check_in = check_in
        self.check_out = check_out

    def create_customer(self):
        """
        Create a new customer.
        """
        customers = self._load_customers()
        customers.append({'name': self.customer_name})
        self._save_customers(customers)

    def delete_customer(self, customer_name):
        """
        Delete a customer.
        """
        customers = self._load_customers()
        customers = [c for c in customers if c['name'] != customer_name]
        self._save_customers(customers)

    def display_customer_info(self):
        """
        Display information about a customer.
        """
        customers = self._load_customers()
        for customer in customers:
            if customer['name'] == self.customer_name:
                print("Customer Name:", customer['name'])
                # Display additional customer information if needed
                break
        else:
            print("Customer not found.")

    def modify_customer_info(self, new_name):
        """
        Modify customer information.
        """
        customers = self._load_customers()
        for customer in customers:
            if customer['name'] == self.customer_name:
                customer['name'] = new_name
                break
        self._save_customers(customers)

    def _load_customers(self):
        """
        Load customer data from a JSON file.
        """
        try:
            with open("customers.json", 'r', encoding='utf-8') as f:
                customers = json.load(f)
        except FileNotFoundError:
            customers = []
        return customers

    def _save_customers(self, customers):
        """
        Save customer data to a JSON file.
        """
        with open("customers.json", 'w', encoding='utf-8') as f:
            json.dump(customers, f, indent=4)


class Reservation:
    """
    Represents a reservation.
    """

    def __init__(self, customer_name, hotel_name, room_type, check_in, check_out):
        self.customer_name = customer_name
        self.hotel_name = hotel_name
        self.room_type = room_type
        self.check_in = check_in
        self.check_out = check_out

    def to_json(self):
        """
        Convert reservation data to JSON format.
        """
        return {
            'customer_name': self.customer_name,
            'hotel_name': self.hotel_name,
            'room_type': self.room_type,
            'check_in': self.check_in,
            'check_out': self.check_out
        }

    def create_reservation(self):
        """
        Create a new reservation.
        """
        # Load existing reservations
        reservations = self._load_reservations()
        # Check if the room is available for the given period
        if self._is_room_available(reservations):
            # Add reservation to the list
            reservations.append(self.to_json())
            # Save updated reservations
            self._save_reservations(reservations)
            print("Reservation created successfully.")
        else:
            print("Room is not available for the specified period.")

    def cancel_reservation(self):
        """
        Cancel an existing reservation.
        """
        # Load existing reservations
        reservations = self._load_reservations()

        # Find and remove the reservation
        for idx, reservation in enumerate(reservations):
            if (reservation['customer_name'] == self.customer_name and
                    reservation['hotel_name'] == self.hotel_name and
                    reservation['room_type'] == self.room_type and
                    reservation['check_in'] == self.check_in and
                    reservation['check_out'] == self.check_out):
                del reservations[idx]
                # Save updated reservations
                self._save_reservations(reservations)
                print("Reservation canceled successfully.")
                return

    def _load_reservations(self):
        """
        Load reservation data from a JSON file.
        """
        try:
            with open("reservations.json", 'r', encoding='utf-8') as f:
                reservations = json.load(f)
        except FileNotFoundError:
            reservations = []
        return reservations

    def _save_reservations(self, reservations):
        """
        Save reservation data to a JSON file.
        """
        with open("reservations.json", 'w', encoding='utf-8') as f:
            json.dump(reservations, f, indent=4)

    def _is_room_available(self, reservations):
        """
        Check if the room is available for the given period.
        """
        check_in_date = datetime.strptime(self.check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(self.check_out, "%Y-%m-%d")

        for reservation in reservations:
            reservation_check_in = datetime.strptime(reservation['check_in'], "%Y-%m-%d")
            reservation_check_out = datetime.strptime(reservation['check_out'], "%Y-%m-%d")

            if (self.hotel_name == reservation['hotel_name'] and
                    self.room_type == reservation['room_type'] and
                    (check_in_date < reservation_check_out and check_out_date > reservation_check_in)):
                return False
        return True
