
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from .app import  create_app
from .models import  setup_db, Customer, Rating, Artist


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
        res = self.client().post('/artist', json=self.artist)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_search_question(self):
        """TEST Case for searching for a question, it will return 200 if success"""
        res = self.client().post('/questions/search', json={"searchTerm":"Who"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['questions'])),
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])



    def test_get_questions(self):
        """Testing Get Question method, this test should retrieve all questions in db, if suceess it will return 200"""
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])

    def test_get_questions_paginated(self):
        """Testing Get Question method, this test should retrieve all questions in db, if suceess it will return 200"""
        res = self.client().get('/questions?=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])


    def test_get_categories(self):
        """Testing Get Categories method, this test should retreive all Categories in db, if suceess it will return 200"""
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(data['categories'])

    def test_get_question_by_category(self):
        """Testing Get Question by category method, this test should retreive all questions in choosen category in db, if suceess it will return 200"""
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])



    def test_delete_question(self):
        """Testing Get Question method, this test should retreive all questions in db, if suceess it will return 200"""
        res = self.client().delete('/questions/24')

        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 24).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertEqual(question,None)


    def test_play(self):
        """Testing Play quiz method, takes previous question and category , this test should check for previous questions and retrieve random it will return the question and success"""

        res = self.client().post('/quizzes?category=1', json=self.previous)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_404_get_pegnatied(self):
        """Testing Get Question method, this test should retrieve all questions in db, if suceess it will return 200"""
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])




    def test_404_delete(self):
        """TEST case for 404 delete, if deletion is not sucessful it will retuen 404"""
        res = self.client().delete('/questions/79oq83kljljlk09903284kejflkj')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_404_get_question_by_category(self):
        """Test for get question by category if not sucessful it should return 404"""
        res = self.client().get('/categories/sadqwdjmlkajwdfkjd/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_404_search(self):
        """TEST case for searching, it should return 404 if something is not found"""
        res = self.client().post('/questions/search', json={"searchTerm":"dsjkahajdsajkwlkjdkjwiqureoiuo3uiurfkndjkhf"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertTrue(data['message'])


    def test_422_create_question(self):
        """Testing create question with empty value of one of the keys, it should return 422"""

        res = self.client().post('/questions', json={"category":''})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()