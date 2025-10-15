import unittest
import json
from flaskHttpServer import app

class TestFlaskPubSub(unittest.TestCase):
    
    def setUp(self):
        """Set up test client before each test"""
        self.app = app.test_client()
        self.app.testing = True
        
        # Clear subscribers before each test
        with app.app_context():
            from flaskHttpServer import subscribers
            subscribers.clear()
    
    def test_root_endpoint(self):
        """Test the root endpoint returns proper response"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('main endpoint', data)
    
    def test_add_subscriber(self):
        """Test adding a subscriber"""
        payload = {
            'name': 'Alice',
            'URI': 'http://alice.example.com'
        }
        response = self.app.post('/add-subscriber',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('Alice', data['message'])
    
    def test_list_subscribers_empty(self):
        """Test listing subscribers when none exist"""
        response = self.app.get('/list-subscribers')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)
    
    def test_list_subscribers_with_data(self):
        """Test listing subscribers after adding some"""
        # Add two subscribers
        self.app.post('/add-subscriber',
                     data=json.dumps({'name': 'Bob', 'URI': 'http://bob.com'}),
                     content_type='application/json')
        self.app.post('/add-subscriber',
                     data=json.dumps({'name': 'Charlie', 'URI': 'http://charlie.com'}),
                     content_type='application/json')
        
        # List subscribers
        response = self.app.get('/list-subscribers')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data['Bob'], 'http://bob.com')
        self.assertEqual(data['Charlie'], 'http://charlie.com')
    
    def test_delete_subscriber(self):
        """Test deleting a subscriber"""
        # First add a subscriber
        self.app.post('/add-subscriber',
                     data=json.dumps({'name': 'David', 'URI': 'http://david.com'}),
                     content_type='application/json')
        
        # Delete the subscriber
        response = self.app.delete('/delete-subscriber',
                                   data=json.dumps({'name': 'David'}),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        # Verify it's gone
        list_response = self.app.get('/list-subscribers')
        data = json.loads(list_response.data)
        self.assertNotIn('David', data)
    
    def test_delete_nonexistent_subscriber(self):
        """Test deleting a subscriber that doesn't exist"""
        response = self.app.delete('/delete-subscriber',
                                   data=json.dumps({'name': 'NonExistent'}),
                                   content_type='application/json')
        # This should raise an error in current implementation
        # You might want to handle this more gracefully
        self.assertNotEqual(response.status_code, 200)
    
    def test_update_and_notify(self):
        """Test updating subject and notifying subscribers"""
        # Add subscribers first
        self.app.post('/add-subscriber',
                     data=json.dumps({'name': 'Eve', 'URI': 'http://eve.com'}),
                     content_type='application/json')
        self.app.post('/add-subscriber',
                     data=json.dumps({'name': 'Frank', 'URI': 'http://frank.com'}),
                     content_type='application/json')
        
        # Update and notify
        payload = {'subject-update': 'New Topic: Flask is Awesome'}
        response = self.app.post('/update-and-notify',
                                data=json.dumps(payload),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('Flask is Awesome', data['message'])
    
    def test_add_multiple_subscribers_same_name(self):
        """Test that adding subscriber with same name updates the URI"""
        # Add subscriber
        self.app.post('/add-subscriber',
                     data=json.dumps({'name': 'Grace', 'URI': 'http://grace1.com'}),
                     content_type='application/json')
        
        # Add again with same name but different URI
        self.app.post('/add-subscriber',
                     data=json.dumps({'name': 'Grace', 'URI': 'http://grace2.com'}),
                     content_type='application/json')
        
        # Check that only one exists with updated URI
        response = self.app.get('/list-subscribers')
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data['Grace'], 'http://grace2.com')

if __name__ == '__main__':
    unittest.main(verbosity=2)