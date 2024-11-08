from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')
db = client['mongopractise08']
collection = db['users']


@app.route('/home',methods= ['GET'])
def homepage():
   return "INSIDE USRES"

userIdCounter = 1

@app.route('/api/users', methods = ['POST'])
def create_users():
    global userIdCounter
    new_user = request.get_json()
    new_user['_id'] = userIdCounter
    collection.insert_one(new_user)
    userIdCounter +=1
    return jsonify({
        "message":"User added succefully"
    }), 201


@app.route('/api/users', methods = ['GET'])
def getUsers():
    users = collection.find()
    user_list = []
    for user in users:
        user['_id'] = str(user['_id'])
        user_list.append(user)
    return jsonify(user_list)


@app.route('/api/users/<int:user_id>')
def getUserById(user_id):
    user = collection.find_one({"_id": user_id})
    if user:
        return jsonify(user)
    return jsonify({"error": "user not found"}), 404


@app.route('/api/users/<int:user_id>', methods = ['PUT'])
def updateUser(user_id):
    data = request.get_json()
    result = collection.update_one({"_id": user_id}, {"$set": data})
    if result.matched_count > 0:
        return jsonify({"message": "Record update succussfull"})
    return jsonify({"error": "user not found"}), 404

@app.route('/api/users/<int:user_id>', methods = ['DELETE'])
def deleteUser(user_id):
    data = collection.delete_one({"_id": user_id})
    if data.deleted_count > 0:
        return({"message": "record deleted succesfully"}), 200
    return jsonify({"error": "user not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)