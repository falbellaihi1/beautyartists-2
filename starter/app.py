import os
from flask import Flask, request, jsonify, abort
from pip._vendor import requests
from sqlalchemy import exc
import json
from flask_cors import CORS
from .models import setup_db, db_drop_and_create_all, create_db, Stylist

from functools import wraps


def create_app(test_config=None):  # create app
    app = Flask(__name__)
    setup_db(app)
    # CORS(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    '''
    @TODO uncomment the following line to initialize the datbase
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    '''
    #db_drop_and_create_all()
    create_db()
    @app.after_request
    def after_request(response):  # after request header decorators
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response



    ## ROUTES

    ####################################
    '''
    @TODO implement endpoint     'DONE'
        GET /stylists
            it should be a public endpoint
            it should contain only the stylist.short() data representation
        returns status code 200 and json {"success": True, "stylists": stylists} where stylists is the list of stylists
            or appropriate status code indicating reason for failure
    '''

    @app.route("/")
    def home_view():
        return "<h1>Wlecome to Hairstylists reviews</h1>"


    @app.route('/stylists', methods=['GET'])
    def get_stylists():  # public get stylist, requires no permission, it retrieves all stylists in short format

        return jsonify(
            {
                "sucess":True,
                "message":"Getting list"
            }
        )

    '''
    @TODO implement endpoint     
        GET /stylists-detail
            it should require the 'get:stylists-detail' permission
            it should contain the stylist.long() data representation
        returns status code 200 and json {"success": True, "stylist": stylists} where stylists is the list of stylists
            or appropriate status code indicating reason for failure
    '''

    @app.route('/stylists-detail',
               methods=['GET'])  
    #@requires_auth('get:stylists-detail')
    def detail_stylists(playload):
        try:

            stylists = Stylist.query.all()
            if stylists:
                long_stylists = [stylist.long() for stylist in stylists]
            else:
                long_stylists = []
            return jsonify({"success": True, "stylists": long_stylists})
        except:
            abort(401)

    '''
    @TODO implement endpoint      'DONE'
        POST /stylists
            it should create a new row in the stylists table
            it should require the 'post:stylists' permission
            it should contain the stylist.long() data representation
        returns status code 200 and json {"success": True, "stylists": stylist} where stylist an array containing only the newly created stylist
            or appropriate status code indicating reason for failure
    '''

    @app.route('/stylists', methods=['POST'])
    #@requires_auth('post:stylists')
    def add_stylists(payload):
        return 'None'


    '''
    @TODO implement endpoint
        PATCH /stylists/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:stylists' permission
            it should contain the stylist.long() data representation
        returns status code 200 and json {"success": True, "stylists": stylist} where stylist an array containing only the updated stylist
            or appropriate status code indicating reason for failure
    '''

    @app.route('/stylists/<int:id>', methods=['PATCH'])
    #@requires_auth('patch:stylists')
    def edit_stylist(payload, id):
       return 'None'

    '''
    @TODO implement endpoint
        DELETE /stylists/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:stylists' permission
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''

    @app.route('/stylists/<int:id>', methods=['DELETE'])
    #@requires_auth('delete:stylists')
    def delete_stylist(playload, id):
        return 'None'

    ## Error Handling
    '''
    Example error handling for unprocessable entity
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(401)
    def authorization(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "you do not have the permissions to do this action"
        }), 401

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422
    '''
    @TODO implement error handler for 404
        error handler should conform to general task above 
    '''
    '''
    @TODO implement error handlers using the @app.errorhandler(error) decorator
        each error handler should return (with approprate messages):
                 jsonify({
                        "success": False, 
                        "error": 404,
                        "message": "resource not found"
                        }), 404

    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500





    '''
    @TODO implement error handler for AuthError
        error handler should conform to general task above 
    '''

    # @app.errorhandler(AuthError)
    # def auth_error(error): # handle auth errors and returns it as json
    #     print('tb')
    #     print(error.status_code)
    #     print(error.error)
    #     return jsonify({
    #         "success": False,
    #         "error": error.status_code,
    #         "message": error.error
    #
    #     }), error.status_code

    return app



