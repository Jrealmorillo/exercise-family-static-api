"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/addmember', methods=['POST'])
def new_member():   
    jackson_family.add_member(request.json)

    return jsonify('New member added'), 200

@app.route('/deletemember/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    response = jackson_family.delete_member(member_id)

    return jsonify('Member successfully deleted'), 200

@app.route('/getmember/<int:member_id>', methods=["GET"])
def get_member(member_id):
    response = jackson_family.get_member(member_id)

    return jsonify(response), 200

@app.route('/updatemember/<int:member_id>', methods=["PUT"])
def update_member(member_id):
    response = jackson_family.update_member(member_id, request.json)

    return jsonify('Member successfully updated'), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
