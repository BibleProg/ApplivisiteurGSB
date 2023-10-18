from flask import Flask,request,jsonify,session, make_response, render_template
from flask_restful import Api,Resource
from security import auth,identity
from flask_jwt import JWT,jwt_required
from user import SignUp

app = Flask(__name__)
app.secret_key = 'JSIZKODLPSZMDM¨D5E6D56ED65E56D56556'
api = Api(app)
jwt = JWT(app,auth,identity)
items = []

class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404
    def post(self,name):
        if next(filter(lambda x:x['name'] == name,items),None):
            return {'message':'le médicament '+name+' existe déjà'}
        data = request.get_json()
        new_item = {'name':name,'prix':data['prix']}
        items.append(new_item)
        return new_item
    def delete(self,name):
        global items
        items = list(filter(lambda x:x['name']!=name,items))
        return items
    def put(self,name):
        data = request.get_json()
        item = next(filter(lambda x:x['name'] == name,items),None)
        if item is None:
            item = {'name':name,'prix':data['prix']}
            items.append(item)
        else:
            item.update(data)

class ItemList(Resource):
    def get(self):
        return{'item':items}

api.add_resource(Item,'/items/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(SignUp,'/signup')

app.run(port=4000,debug=True)