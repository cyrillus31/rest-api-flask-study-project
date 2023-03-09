import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required



class Item(Resource):



    @jwt_required() # this is a speciall callable decorator that returns a decorator when called (e.g. some_method = some_decorator()(some_method))
    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        #        return item

        # item = next(filter(lambda x: x["name"] == name, items), None) # when lambda function returns True the item is from items is added to the filter object, and next get the first and only object
        # return {'item': item}, 200 if item else 404

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query, (name, ))
        row = result.fetchone()
        connection.close()

        if row:
            return {
                'item': {
                'name': row[0],
                'price': row[1]
                }
            }
        
        return {
            'message': 'Item not found'
        }, 404
        




    def post(self, name):
        if next(filter(lambda x: x["name"] == name, items), None) is not None:
            return {"message": "an item with name {} already exists".format(items["name"])}, 400
        data = request.get_json() # this allows for your api to access the request's body payload in json
        price = data["price"]
        item = {'name': name, 'price': price}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": "item deleted"}

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price',
                            type=float,
                            required=True,
                            help="This field cannot be left blank!")

        # data = request.get_json() # once you add reqparse.RequestParser() this line should be modified because you will get the payload from the parser now
        data = parser.parse_args()
        item = next(filter(lambda x: x["name"] == name, items), None)
        if item is None:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)
        return item




class Items(Resource):
    def get(self):
        return {"items": items}, 200