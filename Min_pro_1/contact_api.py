from flask import Flask, request
from flask_restful import Resource, Api
import re

app = Flask(__name__)
api = Api(app)

contacts = []
contact_id_counter = 1

def validate_contact(data):
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')
    if not name or not phone:
        return 'Name and phone are required'
    if not re.match(r'^\d{10}$', str(phone)):
        return 'Phone must be exactly 10 digits'
    return None

class ContactList(Resource):
    def get(self):
        return {'contacts': contacts}, 200

    def post(self):
        global contact_id_counter
        data = request.get_json()
        error = validate_contact(data)
        if error:
            return {'error': error}, 400

        contact = {
            'id': contact_id_counter,
            'name': data['name'],
            'phone': data['phone'],
            'email': data.get('email')
        }
        contacts.append(contact)
        contact_id_counter += 1
        return {'message': 'Contact added', 'contact': contact}, 201

class Contact(Resource):
    def get(self, cid):
        for contact in contacts:
            if contact['id'] == cid:
                return contact, 200
        return {'error': 'Contact not found'}, 404

    def put(self, cid):
        data = request.get_json()
        for contact in contacts:
            if contact['id'] == cid:
                contact['name'] = data.get('name', contact['name'])
                phone = data.get('phone', contact['phone'])
                if not re.match(r'^\d{10}$', str(phone)):
                    return {'error': 'Phone must be 10 digits'}, 400
                contact['phone'] = phone
                contact['email'] = data.get('email', contact['email'])
                return {'message': 'Contact updated', 'contact': contact}, 200
        return {'error': 'Contact not found'}, 404

    def delete(self, cid):
        for contact in contacts:
            if contact['id'] == cid:
                contacts.remove(contact)
                return {'message': 'Contact deleted'}, 200
        return {'error': 'Contact not found'}, 404

api.add_resource(ContactList, '/contacts')
api.add_resource(Contact, '/contacts/<int:cid>')

if __name__ == '__main__':
    app.run(debug=True)

