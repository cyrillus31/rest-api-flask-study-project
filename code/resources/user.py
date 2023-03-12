import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel



class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="I don't know what to say!")
    parser.add_argument("password", type=str, required=True, help="You have to have a password!")

    def post(self):
        data = UserRegister.parser.parse_args()

        # checking if the user is already in database
        if UserModel.find_by_username(data["username"]):
            return {"message": "user already exists"}, 400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data["username"], data["password"]))

        connection.commit()
        connection.close()

        return {"message": "user created successfully"}, 201
        


