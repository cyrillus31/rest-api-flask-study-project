import sqlite3
from flask_restful import Resource, reqparse, request
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field cannot be left blank")

    @jwt_required() # this is a speciall callable decorator that returns a decorator when called (e.g. some_method = some_decorator()(some_method))
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        
        return {
            'message': 'ItemModel not found'
        }, 404

    

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "an item with name {} already exists".format(name)}, 400

        data = request.get_json() # this allows for your api to access the request's body payload in json
        price = data["price"]
        item = ItemModel(name, price)
        try:
            item.insert()
        except:
            return {"message": "Something went wrong trying to insert the item into DB"}, 500

        return item.json(), 201

    def delete(self, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        
        query = "DELETE FROM items WHERE name=?"

        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

        return {"message": "item deleted"}

    def put(self, name):
        data = Item.parser.parse_args() #defined at the beginning of the class

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data["price"])
        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "An error occured inserting an item"}, 500
        else:
            try:
                item.update()
            except:
                return {"message": "An error occured updating an item"}, 500

        return updated_item.json()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        rows = cursor.execute("SELECT * FROM items").fetchall()
        items = []

        for row in rows:
            items.append({"name": row[0], "price": row[1]})
        
        connection.close()

        return {"items": items}, 200