from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity
from security import authenticate, identity

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True  # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'ati'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []


@app.route('/')
def hello_world():
    return 'Hello World qw!'


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="Az árat kötelező meghatározni!"
                        )
    # parser.add_argument('valami mező',
    #                     type=float,
    #                     required=True,
    #                     help="Az árat kötelező meghatározni!"
    #                     )

    # @jwt_required()
    def get(self, name):
        # ez lambdával
        # ha van x: x['name'] páros a "items" diktioanryban akkor beáílltja ha nincs akkor None
        # 'item': enként loopolja

        # for/if next(filter(lambda x: x['name'] == name, items), None)
        # külön return {'item': item}, 200 if item else 404
        # a for/if és és return egy sorban:
        return {'item': next(filter(lambda x: x['name'] == name, items), None)}

        # for item in items:
        #     if item['name'] == name:
        #         return item
        # return {'item': None}, 404

    @jwt_required()
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "Ezzel a névvel '{}' már létezik elem.".format(name)}, 400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    @jwt_required()
    def delete(self, name):
        # lokális mező legyen elérhető
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Elem törölve'}

    @jwt_required()
    def put(self, name):
        # mezők elemzése validálással
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

# if __name__ == '__main__':
# app.run(debug=True)  # important to mention debug=True
# run -> edit_conf menü checkbox
# így updateli a browsert

if __name__ == '__main__':
    app.run(port=5000, debug=True)
