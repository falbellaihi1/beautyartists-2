import json
import os

from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from models import setup_db, db_drop_and_create_all, Artist, Rating, db, Customer, create_db
from auth.auth import AuthError, requires_auth, is_authenticated
import http.client
from sqlalchemy import *

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

    ## HELPERS

    def management_api_token():  # retrieves management api token
        print("trying..")
        try:
            CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
            CLIENT_SEC = os.environ.get('AUTH0_CLIENT_SECRET')
            conn = http.client.HTTPSConnection("falbellaihi1.us.auth0.com")
            playload = {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SEC,
                "audience": "https://falbellaihi1.us.auth0.com/api/v2/",
                "grant_type": "client_credentials"
            }
            playload_json = json.dumps(playload)
            # print(playload_json)
            headers = {'content-type': "application/json"}
            conn.request("POST", "/oauth/token", playload_json, headers)
            res = conn.getresponse()
            data = res.read()
            data_loads = json.loads(data)
            token = data_loads['access_token']
            return token
        except:
            abort(404)
    def retrieve_customers():
        customers = Customer.query.all()
        for customer in customers:
            return customer.format()

    def retrieve_artists():
        return [artist.format() for artist in Artist.query.all()]

    ####################################


    def assign_role(role, uid):  # IMPORTANT WHEN USER SIGNS IN FIRST TIME, ROLE IS NOT IMPLEMENTED UNTIL SIGNS OUT AND SIGNS IN AGAIN!, FRONTEND HAS TO REJECT USER LOGIN IF NOT SUCCESSFUL HERE!
        print(role)
        auth = management_api_token()
        headers = {'content-type': "application/json",'authorization': 'Bearer {}'.format(auth), 'cache-control': "no-cache"}
        conn = http.client.HTTPSConnection("falbellaihi1.us.auth0.com")
        ########## read existing roles in auth0 ########
        conn.request("GET", "/api/v2/roles", headers=headers)
        existing_roles_response = conn.getresponse()
        read_response = existing_roles_response.read()
        existing_roles = json.loads(read_response.decode("utf-8"))

        ####### read user current roles ######
        conn.request("GET", "/api/v2/users/{}/roles".format(uid), headers=headers)
        user_roles_res = conn.getresponse();
        read_user_roles = user_roles_res.read()
        json_user_roles = json.loads(read_user_roles.decode("utf-8"))
        if(len(json_user_roles) > 0):
            print( ' you already have roles ----> ' ,json_user_roles)
            conn.close()
        if (len(json_user_roles) == 0):
            print('no roles, creating one now')
            for i in range(len(existing_roles)):
                if existing_roles[i]['name'] == role:
                    print('assigning', existing_roles[i]['id'])
                    payload = {
                        "roles": [existing_roles[i]['id']]
                    }
                    conn.request("POST", "/api/v2/users/{}/roles".format(uid), json.dumps(payload) ,headers=headers)
                    res = conn.getresponse()
                    data = res.read()
                    print(data.decode("utf-8"))
                    conn.close()




    '''
    @TODO implement endpoint     'DONE'
        GET /stylists
            it should be a public endpoint
            it should contain only the stylist.short() data representation
        returns status code 200 and json {"success": True, "stylists": stylists} where stylists is the list of stylists
            or appropriate status code indicating reason for failure
    '''

    #
    # def get_rated_stylists_helper():
    #     data = []
    #
    #     rates = db.session.query(Rating).join(Stylist).all()
    #     print(rates)

    @app.route("/")
    def home_view():
        return "<h1>Wlecome to Hairstylists reviews</h1>"



    '''
    @TODO implement endpoint      'DONE'
        POST /stylists
            it should create a new row in the stylists table
            it should require the 'post:stylists' permission
        returns status code 200 and json {"success": True, "stylists": stylist} where stylist an array containing only the newly created stylist
            or appropriate status code indicating reason for failure
    '''

    @app.route('/artists/<int:id>/user', methods=['GET'])
    def get_by_id_artists(id):  # public get stylist, requires no permission, it retrieves all stylists and rating
        try:
            artist = Artist.query.filter(Artist.id == id).one_or_none()
            print(artist)
            return jsonify({"success": True, "id": artist.format()})
        except Exception as e:
            print(e)
            abort(404)

    @app.route('/artist', methods=['POST'])
    # no need for authentication since the rule comes after the registeration!
    # @requires_auth('post:stylists')
    @is_authenticated()
    def create_artist(playload):
        try:
            get_artist = Artist.query.filter_by(email=request.json.get('email')).first()
            if (get_artist is not None):
                print('existing user ',get_artist.format())
                return jsonify({
                    "success": True,
                    "artist": [get_artist.format()]
                })

            else:  # else if user does not have record create a record of the user
                # assign_role(request.json.get('role'))
                new_artist = Artist(
                    name=request.json.get('name'),
                    email=request.json.get('email'),
                    auth_user_id=request.json.get('authuid'),
                    speciality=request.json.get('speciality'))
                Artist.insert(new_artist)

            query_artists = Artist.query.filter(Artist.id == new_artist.id).one_or_none()
            print('new user ', query_artists.format(), playload['sub'])
            assign_role('artist', playload['sub'])
            return jsonify({
                "success": True,
                "artist": [query_artists.format()]
            })

        except Exception as e:
            print(e)
            abort(401)

    @app.route('/customer', methods=['POST'])
    @is_authenticated()
    def create_customer(playload):  # CUSTOMER ID NEEDS TO BE PASSED HERE,
        # IMPORTANT encrypt jwt in auth0 rule

        print("role is ", request.json)
        try:
            print(type(request.json.get('email')))
            get_customer = Customer.query.filter_by(email = request.json.get('email')).first()

            if(get_customer is not None):
                print(get_customer)
                return jsonify({
                        "success": True,
                        "customer": [get_customer.format()]
                    })

            else:  # else if user does not have record create a record of the user
                print('else')
                new_customer = Customer(
                    name=request.json.get('name'),
                    email=request.json.get('email'),
                    auth_user_id=request.json.get('authuid')

                )
                # registering using frontend, complete the user info from playload
                Customer.insert(new_customer)
                assign_role(role='customer', uid=new_customer.auth_user_id)
                print('role assigned')
                query_customer = Customer.query.filter(Customer.id == new_customer.id).one_or_none()
                return jsonify({
                    "success": True,
                    "customer": [query_customer.format()]
                })

        except Exception as e:
            print(e)
            abort(401)

    @app.route('/artists', methods=['GET'])
    def get_artists():
        try:
            artists = Artist.query.all()
            formatted_artist = [artist.format() for artist in artists]

            return jsonify({
                "success": True,
                "artist": [formatted_artist]
            })
        except Exception as e:
            print(e)
            abort(404)
    @app.route('/customer', methods=['GET'])
    def get_customer():
        try:
            customers = Customer.query.all()
            formatted_customer = [customer.format() for customer in customers]
            return jsonify({
                "success": True,
                "customer": [formatted_customer]
            })
        except Exception as e:
            print(e)
            abort(404)




    @app.route('/customer/<int:id>', methods=['PATCH'])
    @requires_auth('patch:customer')
    def edit_customer(payload, id):
        try:
            customer = Customer.query.filter(Customer.id == id).one_or_none()
            if not customer:
                abort(404)
            customer.name = request.json.get('name')
            customer.email = request.json.get('email')
            Customer.update(customer)
            updated_customer = Customer.query.filter(Customer.id == id).one_or_none()

            return jsonify({
                "success": True,
                "customer": [updated_customer.format()]
            })
        except Exception as e:
            print(e)
            abort(401)

    '''
    @TODO implement endpoint
        PATCH /stylists/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:stylists' permission
            it should contain the stylist data representation
        returns status code 200 and json {"success": True, "stylists": stylist} where stylist an array containing only the updated stylist
            or appropriate status code indicating reason for failure
    '''

    @app.route('/artists/<int:id>', methods=['PATCH'])
    @requires_auth('patch:artist')
    def edit_artist(payload, id):
        try:
            artist = Artist.query.filter(Artist.id == id).one_or_none()
            print(artist)
            if not artist:
                abort(404)
            artist.name = request.json.get('name')
            artist.speciality = request.json.get('speciality')
            artist.image_link = request.json.get('image_link')
            Artist.update(artist)
            updated_artist = Artist.query.filter(Artist.id == id).one_or_none()

            return jsonify({
                "success": True,
                "artist": [updated_artist.format()]
            })
        except Exception as e:
            print(e)
            abort(401)

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

    @app.route('/artist/<int:id>', methods=['DELETE'])
    @requires_auth('delete:artist')
    def delete_artist(playload, id):
        try:
            artist = Artist.query.filter(Artist.id == id).one_or_none()
            if not artist:
                abort(404)
            else:
                artist.delete()
                return jsonify({
                    "success": True,
                    "deleted": id,
                })
        except Exception as e:
            print(e)
            abort(401)

    @app.route('/customer/<int:id>', methods=['DELETE'])
    @requires_auth('delete:customer')
    def delete_customer(playload, id):
        try:
            customer = Customer.query.filter(Customer.id == id).one_or_none()
            if not customer:
                abort(404)
            else:
                customer.delete()
                return jsonify({
                    "success": True,
                    "deleted": id,
                })
        except Exception as e:
            print(e)
            abort(401)

    @app.route('/review', methods=['POST'])
    @requires_auth('post:review')
    def rate_artist(playload):
        try:
            customer_rating = Customer.query.filter(Customer.auth_user_id == playload['sub']).one_or_none()
            artist_rating = Artist.query.filter(Artist.id == request.json.get('artist_id')).one_or_none()
            if not artist_rating:
                abort(404)
            new_rating = Rating(rate=request.json.get('rate'), artist_id=request.json.get('artist_id'),
                                comment=request.json.get('comment'), customer_id=customer_rating.id)
            Rating.insert(new_rating)
            ratings = [rate.format() for rate in Rating.query.all()]
            print(ratings)
            return jsonify({
                "success": True,
                "ratings": ratings
            })
        except Exception as e:
            print(e)
            abort(404)


    @app.route('/review/<int:id>', methods=['PATCH'])
    @requires_auth('patch:review')
    def edit_review(payload, id): # IMPORTANT user can edit only the comment created by the user not other users!
        try:
            customer_name = payload['http://localhost:8100/info'][1]
            print('customer editing   .... ',customer_name)
            review = Rating.query.filter_by(id=id).join(Customer).filter_by(name=customer_name).first()
            artist = Artist.query.filter_by(id=request.json.get('artist_id')).one_or_none()
            if not review or not artist:
                abort(404)
            review.rate = request.json.get('rate')
            review.comment = request.json.get('comment')
            review.artist_id = request.json.get('artist_id')
            Rating.update(review)
            updated_review = Rating.query.filter(Rating.id == id).one_or_none()

            return jsonify({
                "success": True,
                "artist": [updated_review.format()]
            })
        except Exception as e:
            print(e)
            abort(404)
    
    @app.route('/review/<int:id>', methods=['DELETE'])
    @requires_auth('delete:review')
    def delete_review(playload, id):
        try:
            review = Rating.query.filter(Rating.id == id).one_or_none()
            if not review:
                abort(404)
            else:
                review.delete()
                return jsonify({
                    "success": True,
                    "deleted": id,
                })
        except Exception as e:
            print(e)
            abort(401)

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

    @app.errorhandler(AuthError)
    def auth_error(error):  # handle auth errors and returns it as json
        print('tb')
        print(error.status_code)
        print(error.error)
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error

        }), error.status_code

    return app


if __name__ == "__main__":
    create_app().run()
