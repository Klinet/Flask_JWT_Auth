from flask import Flask, request, render_template
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity
from security import authenticate, identity
import pymysql

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True  # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'ati'
api = Api(app)

jwt = JWT(app, authenticate, identity)


# connection = sqlite3.connect('db/users.db')
#
# cursor = connection.cursor()
#
# create_table = "CREATE TABLE users (id int, username text, password text, jwtoken text)"
# cursor.execute(create_table)
#
# new_user = (1, 'Elek', 'teszt', 'token123')
# insert_query = "insert into users values (?, ?, ?, ?)"
# cursor.execute(insert_query, new_user)

class Database:
    def __init__(self):
# this db cred

        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()

    def list_users(self):
        self.cur.execute("SELECT * FROM users LIMIT 1")
        result = self.cur.fetchall()

        return result


@app.route('/a')
def users():
    def db_query():
        db = Database()
        emps = db.list_users()

        return emps

    res = db_query()

    return render_template('index.html', result=res, content_type='application/json')


items = []


#
# @app.route('/')
# def hello_world():
#     return 'Hello World qw!'


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
