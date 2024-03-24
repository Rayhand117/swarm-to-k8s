import os
import sys
from unittest import TestCase, mock

sys.path.append('web-vote-app')  # add the path where app.py is located
from app import app  # import the actual application

class TestAppRoutes(TestCase):
    """App Routes Tests"""

    def setUp(self):
        """Runs before each test"""
        os.environ['WEB_VOTE_NUMBER'] = '1'  # add this line
        self.app = app
        self.app.testing = True  # enable testing mode
        self.client = self.app.test_client()

        # Create a mock Redis object
        self.redis = mock.Mock()

        # Patch the connect_to_redis function to return the mock Redis object
        self.redis_patch = mock.patch('app.connect_to_redis', return_value=self.redis)
        self.redis_patch.start()

    def tearDown(self):
        """Runs after each test"""
        # Stop patching the connect_to_redis function
        self.redis_patch.stop()

    def test_dump_env(self):
        """It should return environment variables"""
        response = self.client.get("/env")
        self.assertEqual(response.status_code, 200)

        # Check for some expected environment variables in the response
        self.assertIn('PATH', response.data.decode())
        self.assertIn('HOSTNAME', response.data.decode())

    def test_index_route(self):
        """Test the index route"""
        # Make the rpush method do nothing
        self.redis.rpush = mock.Mock()

        # Simulate a GET request
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn('voter_id', response.headers.get('Set-Cookie'))

        # Simulate a POST request
        response = self.client.post("/", data={'vote': 'A'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('voter_id', response.headers.get('Set-Cookie'))
