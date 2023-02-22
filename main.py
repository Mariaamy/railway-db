from dotenv import dotenv_values
from flask import Flask, request
import os
import pymongo


app = Flask(__name__)


#### Set up MongoDB connection

# Hardcoded
# MONGO_URI = 'mongodb://mongo:iVTOhJBmyhvwi4yywWVq@containers-us-west-88.railway.app:6549'

if os.path.exists('.env'):
    # Read from the .env file
    config = dotenv_values('.env')
    MONGO_URI = config['URI']
    client = pymongo.MongoClient(MONGO_URI)

else:
    # Use environmental variables
    MONGO_URI = os.environ.get('MONGO_URL')
    host = os.environ.get('MONGOHOST')
    pw = os.environ.get('MONGOPASSWORD')
    port = os.environ.get('MONGOPORT')
    # port = int(port)
    print(type(port), port)
    user = os.environ.get('MONGOUSER')
    # url = os.environ.get('MONGO_URL')
    client = pymongo.MongoClient(host, port,
                                 password=pw, username=user)

database = client['test']



# Mock database
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
    result = database['contacts'].find_one({"_id": id})
    print(result)
    return result



@app.route('/contacts', methods=['POST'])
def add_contact():
    new_document = request.json
    _name = new_document['name']
    database['contacts'].insert_one({'name':_name})


@app.route('/contacts/<id>', methods=['DELETE'])
def delete_contact(id):
    result = database['contacts'].delete_one({"_id": id})
    deletion_successful = result.deleted_count == 1

    if deletion_successful:
        return {'deletion': deletion_successful, 'id': id}
    return {'deletion': deletion_successful}



if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))  # type: ignore
