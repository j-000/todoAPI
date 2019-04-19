from flask_restful import Resource, reqparse, url_for
from flask_jwt_extended import (jwt_required, get_jwt_identity, get_raw_jwt)
from models import TodoModel
from werkzeug.security import generate_password_hash
from models import User
from datetime import datetime

parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)
parser.add_argument('email', type=str)
parser.add_argument('token', type=str)

class UserRegistration(Resource):
  ''' /registration '''

  def get(self):
    return { 
      "message" : "To register send a POST to /registration with the parameters 'username':string, 'email':string, 'password':string. For more details check the docs.",
      "meta" : {
        "endpoint" : "/registration",
        "methods" : ['GET', 'POST'],
        "parameters" : {
          "GET" : "None",
          "POST" : {
            "username" : "string",
            "email" : "string",
            "password" : "string"
          }
        }
      },
      "docs" : f"{url_for('documentation', _external=True)}"
    }

  def post(self):
    data = parser.parse_args()
    username = data['username']
    email = data['email']
    password = data['password']
    if not username or not email or not password:
      return {"message" : "Some parameters are missing. You need 3: 'username', 'email', 'password'."}
    email_exists = User.fetch(email=email)
    if email_exists:
      return {"message" : f"{email} is already registered. If you need to reset your password, send a GET to /reset for instructions."}
    new_user = User.create_new(username, email, password)
    return {"username" : new_user.username, "email": new_user.email, "created at" : str(datetime.now()) }


class UserAuthentication(Resource):
  ''' /authentication '''

  def get(self):
    return { 
      "message" : "To authenticate send a POST to /authentication with the parameters 'username':string, 'email':string, 'password':string. For more details check the docs.",
      "meta" : {        
        "endpoint" : "/authentication",
        "methods" : ['GET', 'POST'],
        "parameters" : {
          "GET" : "None",
          "POST" : {
            "username" : "string",
            "email" : "string",
            "password" : "string"
          }
        }
      },
      "docs" : f"{url_for('documentation', _external=True)}"  
    }
  
  def post(self):
    data = parser.parse_args()
    username = data['username']
    email = data['email']
    password = data['password']
    if not username or not email or not password:
      return {"message" : "Some parameters are missing. You need 3: 'username', 'email', 'password'."}
    user_exists = User.fetch(email=email)
    if user_exists:
      if user_exists.check_password(password):
        return {"message" : "Success.", "token" : f"{user_exists.get_session_token()}", "expires" : "1 hour" }
      else: 
        return {"message" : "Invalid credentials."}
    else:
      return {"message" : f"{email} could not be found. If you need to register, send a GET to /registration for instructions." }  


class UserRefreshToken(Resource):
  ''' /refresh '''

  def post(self):
    data = parser.parse_args()
    email = data['email']
    token = data['token']
    if not token or not email:
      return {"message" : "token or email missing."}
    user = User.verify_session_token(token)
    if user and user.email == email:
      return {"message" : "Success.", "token" : f"{user.get_session_token()}", "expires" : "1 hour" }
    else:
      return {"message" : "Invalid or expired token. You need to re-authenticate."}


class UserLogout(Resource):
  ''' /logout '''
  def post(self):
    data = parser.parse_args()
    token = data['token']
    if not token:
      return {"message" : "token missing."}
    user = User.verify_session_token(token)
    if not user:
      return {"message" : "token invalid or expired."}
    user.delete_token()
    return {"message" : "Success. You have now logged out. Your token is now invalidated."}
      




      
class Todo(Resource):
  ''' /todo '''
  @jwt_required
  def get(self):
    current_user = get_jwt_identity()
    return {"logged in as": f"{current_user}"}

  def delete(self, todo_id):
    Todo.abort_if_todo_doesnt_exist(todo_id)
    del TODOS[todo_id]
    return '', 204

  def put(self, todo_id):
    args = parser.parse_args()
    task = {'task': args['task']}
    return task, 201




