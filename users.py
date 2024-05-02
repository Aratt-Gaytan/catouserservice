# user.py (user module)
from bson import ObjectId
from flask import Blueprint, jsonify, request
from pymongo import MongoClient

# Cadena de conexión
cadena_conexion = "mongodb+srv://DB_admin:dbadmin1605@cluster0.hhn9kde.mongodb.net/catouserservice"

# Conexión a la base de datos
cliente = MongoClient(cadena_conexion)

# Obtener la colección de tareas
db = cliente["catouserservice"]
users = db["user"]

user = Blueprint('user', __name__)  # Create a Blueprint named 'user'

@user.route("/")
def get_users():
    userslist = users.find()
    
    users_json = []
    for user in userslist:
        users_json.append({"_id": str(user["_id"]), "name": str(user["name"]),"phone": str(user["phone"]), "email": str(user["email"]), "birth_date": str(user["birth_date"]), "password": str(user["password"]) })
    # Implement logic to retrieve users
    return jsonify(users_json)

@user.route("/search/<user_email>")
def get_user(user_email):
    search_pattern = f".*{user_email}.*"  # Matches any characters before, after, or containing the email
    email_regex = {"email": {"$regex": search_pattern, "$options": "i"}}  # Case-insensitive search

    # Find users matching the email pattern using regex
    userslist = users.find(email_regex)
    users_json = []
    for user in userslist:
        users_json.append({"_id": str(user["_id"]), "name": str(user["name"]), "email": str(user["email"]), "birth_date": str(user["birth_date"]), "password": str(user["password"]) })
    # Implement logic to retrieve users
    return jsonify(users_json)

   
@user.route("/get/<user_id>")
def get_user_info(user_id):
    # Find users matching the email pattern using regex
    userslist = users.find({"_id": ObjectId(user_id)})
    users_json = []
    for user in userslist:
        users_json.append({"_id": str(user["_id"]), "name": str(user["name"]), "email": str(user["email"]), "birth_date": str(user["birth_date"]), "password": str(user["password"]) })
    # Implement logic to retrieve users
    return jsonify(users_json)


@user.route("/add", methods=["POST"])
def add_user():
    try:
        name = request.form["name"]
        email = request.form["email"]
        birth_date = request.form["birth_date"]
        password = request.form["password"]

        if name or email or birth_date or password:
            # Insertar la nueva tarea en la colección
            users.insert_one({ 'name': name, 'email': email, 'birth_date': birth_date, 'password': password })
        else:
            return jsonify({"message": f"error"}) 

        # Implement logic to retrieve a specific user
        return jsonify({"message": f"User added successfuly"})
    except:
        return jsonify({"message": f"error"})
 

@user.route("/update", methods=["POST"])
def update_user():
    try:
        user_id = request.form.get("user_id")  # Use get() to handle optional parameter
        name = request.form.get("name")
        email = request.form.get("email")
        birth_date = request.form.get("birth_date")
        password = request.form.get("password")

        # Validate user_id presence (optional, adjust based on your requirements)
        if not user_id:
            return jsonify({"message": "Missing required field: user_id"})

        # Construct update document with non-empty fields
        update_data = {}
        if name:
            update_data["name"] = name
        if email:
            # Consider email uniqueness validation here (if applicable)
            update_data["email"] = email
        if birth_date:
            update_data["birth_date"] = birth_date
        if password:
            update_data["password"] = password

        # Check if update data is empty (all fields optional)
        if not update_data:
            return jsonify({"message": "No fields provided for update"})

        # Execute update query using user_id as filter
        update_result = users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})

        # Handle update result and return appropriate response
        if update_result.matched_count == 1:
            return jsonify({"message": "User updated successfully"})
        else:
            return jsonify({"message": "User not found or update failed"})

    except Exception as e:
        print(f"An error occurred: {e}")  # Log the error for debugging
        return jsonify({"message": "Internal server error"}), 500  # Return generic error message



@user.route("/delete", methods=["POST"])
def delete_user():
    try:
        user_id = request.form.get("user_id")

        # Validate user_id presence (optional, adjust based on your requirements)
        if not user_id:
            return jsonify({"message": "Missing required field: user_id"})

        # Execute delete query using user_id as filter
        delete_result = users.delete_one({"_id": ObjectId(user_id)})

        # Handle delete result and return appropriate response
        if delete_result.deleted_count == 1:
            return jsonify({"message": "User deleted successfully"})
        else:
            return jsonify({"message": "User not found or deletion failed"})

    except Exception as e:
        print(f"An error occurred: {e}")  # Log the error for debugging
        return jsonify({"message": "Internal server error"}), 500  # Return generic error message
