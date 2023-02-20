"""Tests for Happy Snacky Server Flask app."""

import unittest
from server import app
import crud
from passlib.hash import argon2



class HappySnacky(unittest.TestCase):
    """Tests for Happy Snacky app"""

    def setUp(self):


        self.client = app.test_client()
        app.config['TESTING'] = True 
        

    def test_homepage(self):
        """Homepage redirect test"""
        

        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h2>Welcome to Happy Snacky!</h2>', result.data)


    def test_login(self):
        """Test user login"""

        
        email = 'test@example.com'
        password = 'test1234'
        fname = 'Test'
        lname = 'User'
        hashed_password = argon2.hash(password)
        crud.create_user(email, hashed_password, fname, lname)

        
        result = self.client.post('/login', data={'email': email, 'password': password}, follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Welcome', result.data)

        
        result = self.client.post('/login', data={'email': email, 'password': 'wrongpassword'}, follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'The email or password you entered was incorrect', result.data)


    def test_logout(self):
        """Test logging out"""

        with self.client as c:
            with c.session_transaction() as session:
                session['user_email'] = 'testuser@example.com'

            result = self.client.post('/logout', data={'logout': True}, follow_redirects=True)

            self.assertEqual(result.status_code, 200)
            self.assertNotIn(b'Logged in as', result.data)
            self.assertIn(b'Logged out.', result.data)

  

    

