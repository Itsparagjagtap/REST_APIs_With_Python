from flask import Flask, jsonify, request

app = Flask(__name__)

users =  [
        {"id": 1, "name": "Parag", "email": "abc@google.com"},
        {"id": 2, "name": "Shankar", "email": "xyz@google.com"},
        {"id": 3, "name": "Amol", "email": "pqr@google.com"},
    ]


@app.route('/',methods= ['GET'])
def homepage():
   return "Home"

@app.route('/api/users', methods = ['GET'])
def getUsers():
    return jsonify(users)

@app.route('/api/users/<int:user_id>', methods = ['GET'])
def getUserById(user_id):
       for user in users:
           if user['id'] == user_id:
               return jsonify(user)
       return jsonify({"error": "user not found"}), 404

@app.route('/api/users', methods = ['POST'])
def create_user():
   new_user = request.get_json()
   new_user['id'] = len(users)+1
   users.append(new_user)
   return jsonify(new_user), 201
    
@app.route('/api/users/<int:user_id>', methods= ['PUT'])
def update_user(user_id):
    for user in users:
        if user['id'] == user_id:
            user.update(request.get_json())
            return jsonify(user), 201
    return jsonify({"error":"user not found" }), 404 


@app.route('/api/users/<int:user_id>', methods= ['DELETE'])
def deleteUser(user_id):
    for user in users:
        if user['id'] == user_id:
            users.remove(user)
            return jsonify({"message": "user deleted"})
    return jsonify({"errors": "user not found"}), 404  


if(__name__ == '__main__'):
    app.run(debug=True)    