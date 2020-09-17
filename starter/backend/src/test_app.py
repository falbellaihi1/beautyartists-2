
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from .app import  create_app
from .models import  setup_db, Customer, Rating, Artist


def get_headers():
    pass


class BeautyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""


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
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()




    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_create_artist(self):
        """Testing create question, if sucess, a question should be created in db"""
        res = self.client().post('/artist', json=self.artist, headers=get_headers())
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_create_customer(self):
        """TEST Case for searching for a question, it will return 200 if success"""
        res = self.client().post('/customer',self.customer, headers=get_headers())
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])



    def test_get_artists(self):
        """Testing Get Question method, this test should retrieve all questions in db, if suceess it will return 200"""
        res = self.client().get('/artists', get_headers())
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['artist'])

    def test_get_customer(self):
        """Testing Get Question method, this test should retrieve all questions in db, if suceess it will return 200"""
        res = self.client().get('/customer', get_headers())
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['customer'])

#IMPORTANT GET REVIEWS TEST




    def test_delete_artist(self):
        """Testing Get Question method, this test should retreive all questions in db, if suceess it will return 200"""
        res = self.client().delete('/artist/24')

        data = json.loads(res.data)
        artist = Artist.query.filter(Artist.id == 24).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertEqual(artist,None)


    # def test_404_artist(self):
    #     """Testing Get artist method, this test should retrieve all artists in db, if suceess it will return 200"""
    #     res = self.client().get('/artist')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'])

    def test_404_delete(self):
        """TEST case for 404 delete, if deletion is not sucessful it will retuen 404"""
        res = self.client().delete('/artists/ssssddddwww')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()