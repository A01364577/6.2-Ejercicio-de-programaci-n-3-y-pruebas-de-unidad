# The next code will follow and implement the set of requirements
# provided for the code implementation.

# Req1.  Implement a set of classes in Python that
# implements two abstractions:
# 1. Hotel
# 2. Reservation
# 3. Customers


import json
# Hotel class implementation
class Hotel:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.rooms = []
        self.reservations = []

    def create_hotel(self):
        hotels = self._load_hotels()
        hotels.append(self.__dict__)
        self._save_hotels(hotels)

    def delete_hotel(self, hotel_name):
        hotels = self._load_hotels()
        hotels = [h for h in hotels if h['name'] != hotel_name]
        self._save_hotels(hotels)

    def display_hotel_info(self):
        hotels = self._load_hotels()
        for hotel in hotels:
            if hotel['name'] == self.name:
                print("Hotel Name:", hotel['name'])
                print("Location:", hotel['location'])
                print("Rooms:", ", ".join(hotel['rooms']))
                print("Reservations:", len(hotel['reservations']))
                break
        else:
            print("Hotel not found.")

    def modify_hotel_info(self, new_name, new_location):
        hotels = self._load_hotels()
        for hotel in hotels:
            if hotel['name'] == self.name:
                hotel['name'] = new_name
                hotel['location'] = new_location
                break
        self._save_hotels(hotels)

    def reserve_room(self, reservation):
        hotels = self._load_hotels()
        for hotel in hotels:
            if hotel['name'] == self.name:
                hotel['reservations'].append(reservation)
                break
        self._save_hotels(hotels)

    def cancel_reservation(self, reservation_id):
        hotels = self._load_hotels()
        for hotel in hotels:
            if hotel['name'] == self.name:
                hotel['reservations'] = [r for r in hotel['reservations'] if r['id'] != reservation_id]
                break
        self._save_hotels(hotels)

    def _load_hotels(self):
        try:
            with open("hotels.json", 'r') as f:
                hotels = json.load(f)
        except FileNotFoundError:
            hotels = []
        return hotels

    def _save_hotels(self, hotels):
        with open("hotels.json", 'w') as f:
            json.dump(hotels, f, indent=4)

# Reservation class implementation
class Customer:
    def __init__(self, customer_name, hotel_name, room_type, check_in, check_out):
        self.customer_name = customer_name
        self.hotel_name = hotel_name
        self.room_type = room_type
        self.check_in = check_in
        self.check_out = check_out

    def create_customer(self):
        customers = self._load_customers()
        customers.append({'name': self.customer_name})
        self._save_customers(customers)

    def delete_customer(self, customer_name):
        customers = self._load_customers()
        customers = [c for c in customers if c['name'] != customer_name]
        self._save_customers(customers)

    def display_customer_info(self):
        customers = self._load_customers()
        for customer in customers:
            if customer['name'] == self.customer_name:
                print("Customer Name:", customer['name'])
                # Display additional customer information if needed
                break
        else:
            print("Customer not found.")

    def modify_customer_info(self, new_name):
        customers = self._load_customers()
        for customer in customers:
            if customer['name'] == self.customer_name:
                customer['name'] = new_name
                break
        self._save_customers(customers)

    def _load_customers(self):
        try:
            with open("customers.json", 'r') as f:
                customers = json.load(f)
        except FileNotFoundError:
            customers = []
        return customers

    def _save_customers(self, customers):
        with open("customers.json", 'w') as f:
            json.dump(customers, f, indent=4)

# Customers class implementation
class Reservation:
    def __init__(self, customer_name, hotel_name, room_type, check_in, check_out):
        self.customer_name = customer_name
        self.hotel_name = hotel_name
        self.room_type = room_type
        self.check_in = check_in
        self.check_out = check_out

    def create_reservation(self):
        # Load existing reservations
        reservations = self._load_reservations()

        # Instantiate Customer and Hotel objects
        customer = Customer(self.customer_name)
        hotel = Hotel(self.hotel_name)

        # Check if the room is available for the given period
        if self._is_room_available(reservations):
            # Add reservation to the list
            reservations.append({
                'customer_name': self.customer_name,
                'hotel_name': self.hotel_name,
                'room_type': self.room_type,
                'check_in': self.check_in,
                'check_out': self.check_out
            })
            # Save updated reservations
            self._save_reservations(reservations)
            print("Reservation created successfully.")
        else:
            print("Room is not available for the specified period.")

    def cancel_reservation(self):
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
        print("Reservation not found.")

    def _load_reservations(self):
        try:
            with open("reservations.json", 'r') as f:
                reservations = json.load(f)
        except FileNotFoundError:
            reservations = []
        return reservations

    def _save_reservations(self, reservations):
        with open("reservations.json", 'w') as f:
            json.dump(reservations, f, indent=4)

    def _is_room_available(self, reservations):
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


import unittest
import json
import os

from hotel import Hotel
from customer import Customer
from reservation import Reservation

class TestHotel(unittest.TestCase):
    def setUp(self):
        # Create a temporary test file for reservations
        with open("test_reservations.json", "w") as f:
            json.dump([], f)

    def tearDown(self):
        # Remove the temporary test file after each test
        os.remove("test_reservations.json")

    def test_create_hotel(self):
        # Create a test hotel
        test_hotel = Hotel("Test Hotel", "Test Location")

        # Call create_hotel method
        test_hotel.create_hotel()

        # Load hotels data from file
        with open("hotels.json", 'r') as f:
            hotels_data = json.load(f)

        # Check if the test hotel is in the hotels data
        self.assertTrue(any(hotel['name'] == "Test Hotel" and hotel['location'] == "Test Location" for hotel in hotels_data))

    def test_delete_hotel(self):
        # Create a test hotel
        test_hotel = Hotel("Test Hotel", "Test Location")

        # Call create_hotel method
        test_hotel.create_hotel()

        # Call delete_hotel method to delete the test hotel
        test_hotel.delete_hotel("Test Hotel")

        # Load hotels data from file
        with open("hotels.json", 'r') as f:
            hotels_data = json.load(f)

        # Check if the test hotel is not in the hotels data
        self.assertFalse(any(hotel['name'] == "Test Hotel" for hotel in hotels_data))

    def test_display_hotel_info(self):
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
        Rooms:
        Reservations: 0"""
        self.assertEqual(printed_output, expected_output)


    def test_modify_hotel_info(self):
        # Create a test hotel
        test_hotel = Hotel("Test Hotel", "Test Location")
        test_hotel.create_hotel()

        # Modify the hotel information
        test_hotel.modify_hotel_info("New Hotel Name", "New Location")

        # Load hotels data from file
        with open("hotels.json", 'r') as f:
        hotels_data = json.load(f)

        # Check if the hotel information is modified correctly
        modified_hotel = [hotel for hotel in hotels_data if hotel['name'] == "New Hotel Name"]
        self.assertTrue(modified_hotel)  # Check if there's a hotel with the modified name
        self.assertEqual(modified_hotel[0]['location'], "New Location")  # Check if location is updated


   def test_reserve_room(self):
        # Create a test hotel
        test_hotel = Hotel("Test Hotel", "Test Location")
        test_hotel.create_hotel()

        # Create a test reservation
        reservation_data = {
            'customer_name': "Test Customer",
            'hotel_name': "Test Hotel",
            'room_type': "Single",
            'check_in': "2024-02-20",
            'check_out': "2024-02-25"
        }

        # Reserve a room using reserve_room method
        test_hotel.reserve_room(reservation_data)

        # Load hotels data from file
        with open("hotels.json", 'r') as f:
            hotels_data = json.load(f)

        # Check if the room is reserved for the given reservation
        reserved_room = [reservation for hotel in hotels_data for reservation in hotel['reservations']
                         if reservation['customer_name'] == "Test Customer"]
        self.assertTrue(reserved_room)  # Check if there's a reservation for the test customer


    def test_cancel_reservation(self):
        # Create a test hotel
        test_hotel = Hotel("Test Hotel", "Test Location")
        test_hotel.create_hotel()

        # Create a test reservation
        reservation_data = {
            'customer_name': "Test Customer",
            'hotel_name': "Test Hotel",
            'room_type': "Single",
            'check_in': "2024-02-20",
            'check_out': "2024-02-25"
        }

        # Reserve a room using reserve_room method
        test_hotel.reserve_room(reservation_data)

        # Cancel the reservation using cancel_reservation method
        test_hotel.cancel_reservation(1)  # Assuming the reservation ID is 1

        # Load hotels data from file
        with open("hotels.json", 'r') as f:
            hotels_data = json.load(f)

        # Check if the reservation is canceled
        canceled_reservation = any(reservation['customer_name'] == "Test Customer" for hotel in hotels_data for reservation in hotel['reservations'])
        self.assertFalse(canceled_reservation)  # Check if there's no reservation for the test customer


if __name__ == '__main__':
    unittest.main()



class TestCustomer(unittest.TestCase):

    def setUp(self):
        # Create a test customer
        self.customer_name = "Test Customer"
        customer = Customer(self.customer_name)
        customer.create_customer()

    def tearDown(self):
        # Remove the test customer after each test
        with open("customers.json", 'w') as f:
            json.dump([], f)

    def test_create_customer(self):
        # Test creating a new customer
        new_customer_name = "John Doe"
        customer = Customer(new_customer_name)
        customer.create_customer()

        # Check if the customer is created
        customers = customer._load_customers()
        self.assertTrue(any(c['name'] == new_customer_name for c in customers))

    def test_delete_customer(self):
        # Test deleting an existing customer
        existing_customer_name = "John Doe"
        customer = Customer(existing_customer_name)
        customer.create_customer()

        # Delete the customer
        customer.delete_customer(existing_customer_name)

        # Check if the customer is deleted
        customers = customer._load_customers()
        self.assertFalse(any(c['name'] == existing_customer_name for c in customers))


    def test_display_customer_info(self):
        # Prepare captured output
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Create a customer
        customer_name = "John Doe"
        customer = Customer(customer_name)
        customer.create_customer()

        # Display customer info
        customer.display_customer_info()

        # Reset stdout
        sys.stdout = sys.__stdout__

        # Check if the correct info is displayed
        expected_output = f"Customer Name: {customer_name}\n"
        self.assertEqual(captured_output.getvalue(), expected_output)

    def test_modify_customer_info(self):
        # Create a customer object
        customer = Customer(self.customer_name)

        # Modify customer info
        new_name = "Modified Customer"
        customer.modify_customer_info(new_name)

        # Load customers from file
        with open("customers.json", 'r') as f:
            customers = json.load(f)

        # Check if the customer info is modified
        modified_customer = next((c for c in customers if c['name'] == new_name), None)
        self.assertIsNotNone(modified_customer)
        self.assertEqual(modified_customer['name'], new_name)

if __name__ == '__main__':
    unittest.main()


class TestReservation(unittest.TestCase):
    def setUp(self):
        # Create a temporary test file for reservations
        with open("test_reservations.json", "w") as f:
            json.dump([], f)

    def tearDown(self):
        # Remove the temporary test file after each test
        os.remove("test_reservations.json")

    def test_create_reservation(self):
        # Create a sample reservation
        reservation = Reservation("John Doe", "Hotel ABC", "Single Room", "2024-03-01", "2024-03-05")

        # Call the create_reservation method
        reservation.create_reservation()

        # Load existing reservations from the temporary test file
        with open("test_reservations.json", 'r') as f:
            reservations = json.load(f)

        # Check if the new reservation is in the list of reservations
        self.assertTrue(any(reservation == r for r in reservations), "Reservation was not created.")

    def test_cancel_reservation(self):
        # Create a sample reservation
        reservation = Reservation("Jane Smith", "Hotel XYZ", "Double Room", "2024-04-10", "2024-04-15")

        # Call the create_reservation method to create the reservation
        reservation.create_reservation()

        # Call the cancel_reservation method to cancel the reservation
        reservation.cancel_reservation()

        # Load existing reservations from the temporary test file
        with open("test_reservations.json", 'r') as f:
            reservations = json.load(f)

        # Check if the canceled reservation is not in the list of reservations
        self.assertFalse(any(reservation == r for r in reservations), "Reservation was not canceled.")

if __name__ == '__main__':
    unittest.main()
