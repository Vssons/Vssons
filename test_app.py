import unittest
from flask import Flask
from main import app, con

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.con = con

    def tearDown(self):
        self.con.rollback()

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Employee Management System', response.data)

    def test2_home_page(self):
        response = self.app.get('/')
        self.assertNotEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Employee Management System', response.data)

    def test_get_employees_api(self):
        response = self.app.get('/api/employees')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.get_json()) >= 0)

    def test_add_employee_api(self):
        data = {
            "name": "John Doe",
            "position": "Developer",
            "department": "IT",
            "salary": 60000.00,
            "phone": "123-456-7890",
            "email": "john@example.com",
            "gender": "Male"
        }
        response = self.app.post('/api/add_employee/', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["message"], "Employee Added successfully")

    def test_get_employee_api(self):
        # Assuming there is an employee with id=1 in the database
        response = self.app.get('/api/employee/?emp_id=1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.get_json()) > 0)

if __name__ == '__main__':
    unittest.main()
