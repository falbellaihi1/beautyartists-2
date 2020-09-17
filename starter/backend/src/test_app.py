
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db


def get_headers():
    auth = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNjV0szM2VDZkN4VHczMUo2aHFsWiJ9.eyJodHRwOi8vbG9jYWxob3N0OjgxMDAvcm9sZXMiOlsiYXJ0aXN0Il0sImh0dHA6Ly9sb2NhbGhvc3Q6ODEwMC9pbmZvIjpbImZhbGJlbGxhaWhpMTIzQGdtYWlsLmNvbSIsIkNBVkVNQU4xNTAiLCJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS0vQU9oMTRHaVliMC04Y1dqWWpZUXN5VHQ1Q2dEdVF5UVNzZXh6bkwwaDdkNWJqdyIsbnVsbF0sImlzcyI6Imh0dHBzOi8vZmFsYmVsbGFpaGkxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwNDk3OTIwNDU2MTI0NjkyODE3MCIsImF1ZCI6WyJiZWF1dHlhcnRpc3RzIiwiaHR0cHM6Ly9mYWxiZWxsYWloaTEudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYwMDM1MTI0MSwiZXhwIjoxNjAwMzU4NDQxLCJhenAiOiJ5SXhUVVR0MjlxaXMxek41M3ZzeDZlZmpZN1VrMnA4MCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YXJ0aXN0IiwiZ2V0OmRldGFpbGVkLWN1c3RvbWVyIiwicGF0Y2g6YXJ0aXN0Il19.yK1qghn7v-IQfsVsB5ZpsvO-wR0pcrPwUzpIXi5xHwisj8FRq2SkaszOou7Wor0hmYISSU5tgVlokThJHe8cVfLeFX3KVwAQdGva3qrXa7tcf-J9XYVlqciTowzOdrHMz3q8neFvIX-jJaTcDmAGCRTXFk7SwjC-9VyXTUJPBHCopXaAtvrk61_MJ_HRlHm6fpD1yEmV6ICcQNm5uYaCbE6gYmwHuVX9sYHGVdGjU95pUj08cS_sdtwYhHPGqVr4Y73994W-MBCSmJvWCBb7tE6KK2WhLAihgOs1tbRRCvdHLL68HlYjjS2LRHsF2NOwlSiwp0NjFOlnb4_9US1heQ'
    headers = {'authorization': 'Bearer {}'.format(auth)}

    return headers


class BeautyTestCase(unittest.TestCase):
    """This class represents the beauty  test case"""


    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "beauty_test"
        self.database_path = "postgresql://postgres:0000@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context

        self.new_artist = {
            "name": "Markara",
            "speciality": "Makeup Artist",
            "image_link": "none"

        }
        self.customer = {
            "name": "Markara",
            "email": "Makeup Artist",

        }
        self.rate = {
            "rate" :1,
             "artist_id": 1,
             "comment":"this is a test rating"
        }
        self.rate_404 = {
            "rate": 1,
            "artist_id": 1000,
            "comment": "this is a test rating 404"
        }
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.drop_all()
            self.db.create_all()




    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_create_artist(self):
        """Testing create question, if sucess, a artist should be created in db"""
        res = self.client().post('/artist',json=self.new_artist, headers=get_headers())
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['artist'])




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()