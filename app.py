from ast import Index
from distutils.log import debug
import dbinteractions as db
from flask import Flask, request, Response
import json

app = Flask(__name__)



# GET request for recipes
@app.get('/recipes')
def get_recipes():
    # list of recipes
    recipes = db.get_recipes_db()
    try:
        # convert list to JSON
        if recipes[0] != False:
            recipes_json = json.dumps(recipes, default=str)
            return Response(recipes_json, mimetype="application/json", status=200)
        else:
            return Response(json.dumps(recipes[1], default=str), mimetype='application/json', status=400)
    except Exception as e:
        print(e)
        return Response("Looks like something went wrong, please try again",
                        mimetype="application/json",
                        status=400)


# GET request for users
@app.get('/login')
def attempt_login():
    try:
        username = request.args['username']
        password = request.args['password']
    except KeyError:
        return Response("invalid key name!",
                        mimetype='application/json',
                        status=400)

    try:
        user = db.attempt_login_db(username, password)
        # conditional to see if a user was matched
        if user[0] == False:
            user_json = json.dumps(user[1], default=str)
            return Response(user_json, mimetype="application/json", status=400)
        else:
            user_json = json.dumps(user, default=str)
            return Response(user_json, mimetype="application/json", status=200)
    except Exception as e:
        print(e)
        return Response("looks like we couldn't verify you credentials",
                        mimetype="application/json",
                        status=400)


# GET request for recipe_star
@app.get('/recipe_star')
def get_recipe_star():
    try:
        recipes_id = request.args['recipes_id']
    except KeyError:
        return Response("invalid key name!",
                        mimetype='application/json',
                        status=400)

    try:
        recipe_star = db.get_recipe_star_db(recipes_id)
        if recipe_star[0] == False:
            recipe_star_json = json.dumps(recipe_star[1], default=str)
            return Response(recipe_star_json,
                            mimetype="application/json",
                            status=200)
        else:
            recipe_star_json = json.dumps(recipe_star, default=str)
            return Response(recipe_star_json,
                            mimetype='application/json',
                            status=200)
    except IndexError:
        return Response("looks like this recipe isn't likeable",
                        mimetype="application/json",
                        status=200)
    except Exception as e:
        print(e)
        return Response(
            "looks like we ran into an error processing your request",
            mimetype="application/json",
            status=400)


# POST request for users
@app.post('/users')
def post_users():
    try:
        username = request.json['username']
        password = request.json['password']
    except KeyError:
        return Response("invalid key name!",
                        mimetype='application/json',
                        status=400)
    try:
        user = db.post_users_db(username, password)
        if user[0]:
            user_json = json.dumps(user, default=str)
            return Response(user_json, mimetype='application/json', status=200)
    except Exception as e:
        print(e)


app.run(debug=True)
