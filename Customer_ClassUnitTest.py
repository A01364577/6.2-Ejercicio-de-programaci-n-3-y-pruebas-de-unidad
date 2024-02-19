import unittest
from io import StringIO
import sys
from A01364577_A6_2 import Customer


class TestCustomer(unittest.TestCase):
    """
    Test cases for the Customer class.
    """

    def setUp(self):
        """
        Set up a test customer object.
        """
        self.test_customer = Customer("John Doe", "Test Hotel", "Single", "2024-02-20", "2024-02-25")

    def test_create_customer(self):
        """
        Test creating a customer.
        """
        self.test_customer.create_customer()
        customers = self.test_customer._load_customers()
        self.assertTrue(any(customer['name'] == 'John Doe' for customer in customers))

    def test_delete_customer(self):
        """
        Test deleting a customer.
        """
        self.test_customer.create_customer()
        self.test_customer.delete_customer("John Doe")
        customers = self.test_customer._load_customers()
        self.assertFalse(any(customer['name'] == 'John Doe' for customer in customers))

    def test_display_customer_info(self):
        """
        Test displaying customer information.
        """
        captured_output = StringIO()
        sys.stdout = captured_output

        self.test_customer.create_customer()
        self.test_customer.display_customer_info()
        sys.stdout = sys.__stdout__

        expected_output = "Customer Name: John Doe\n"
        self.assertEqual(captured_output.getvalue(), expected_output)

    def test_modify_customer_info(self):
        """
        Test modifying customer information.
        """
        self.test_customer.create_customer()
        self.test_customer.modify_customer_info("Jane Doe")
        customers = self.test_customer._load_customers()
        self.assertTrue(any(customer['name'] == 'Jane Doe' for customer in customers))


if __name__ == '__main__':
    unittest.main()
