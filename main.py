from dotenv import dotenv_values
from flask import Flask, request
import os
import pymongo

host = os.environ.get('MONGOHOST')
pw = os.environ.get('MONGOPASSWORD')
port = int(os.environ.get('MONGOPORT'))
user = os.environ.get('MONGOUSER')
MONGO_URI = os.environ.get('MONGO_URL')

if os.path.exists('.env'):
    config = dotenv_values('.env')
    MONGO_URI = config['URI']

else:
    MONGO_URI = os.environ.get('URI')


app = Flask(__name__)

# MongoDB conn
config = dotenv_values('.env')
MONGO_URI = config['URI']
client = pymongo.MongoClient(MONGO_URI)
database = client['test']

# database.db.drop_collection('contacts')
# database.db.create_collection('contacts')
contacts = [
    {'_id': '1', 'name': 'Alice'},
    {'_id': '2', 'name': 'Bob'},
    {'_id': '3', 'name': 'Eve'}
]

for contact in contacts:
    print('Adding contact', contact)
    database.db['contacts'].insert_one(contact)


CONTACTS = [{"name": "Paul"}, {"name": "Mary"}, {"name": "John"}]


@app.route('/')
def index():
    return 'Hello Flask!'


@app.route('/contacts')
def get_contacts():
    result = []
    for document in database['contacts'].find({}):
        result.append(document)
    return result


@app.route('/contacts/<id>')
def get_contact(id):
    return CONTACTS[int(id)]


@app.route('/contacts', methods=['POST'])
def update_contact():
    name = request.json['name']
    contact = {"name": name}
    CONTACTS.append(contact)

    id = len(CONTACTS) - 1
    return {'id': id}


@app.route('/contacts/<id>', methods=['DELETE'])
def delete_contact(id):
    del CONTACTS[int(id)]
    return  {'id': id}


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))  # type: ignore
