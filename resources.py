from flask_restful import Resource, reqparse, url_for, request
from models import TodoModel
from werkzeug.security import generate_password_hash
from models import User
from datetime import datetime
from decorators import jwt_required

parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)
parser.add_argument('email', type=str)
parser.add_argument('token', type=str)
parser.add_argument('body', type=str)
parser.add_argument('status', type=str)

api_docs = {"documentation" : "http://localhost:5000/documentation"}


class UserRegistration(Resource):
  ''' /registration '''

  def post(self):
    data = parser.parse_args()
    username = data['username']
    email = data['email']
    password = data['password']
    if not username or not email or not password:
      return {"message" : "Some parameters are missing. You need 'username', 'email' and 'password'.", "meta" : api_docs}
    email_exists = User.fetch(email=email)
    if email_exists:
      return {"message" : f"{email} is already registered. If you need to reset your password, check the docs.", "meta" : api_docs}
    new_user = User.create_new(username, email, password)
    return {"username" : new_user.username, "email": new_user.email, "created at" : str(datetime.now()), "meta" : api_docs }


class UserAuthentication(Resource):
  ''' /authentication '''
  
  def post(self):
    data = parser.parse_args()
    username = data['username']
    email = data['email']
    password = data['password']
    if not username or not email or not password:
      return {"message" : "Some parameters are missing. You need 'username', 'email' and 'password'.", "meta" : api_docs}
    user_exists = User.fetch(email=email)
    if user_exists:
      if user_exists.check_password(password):
        return {"message" : "Success.", "token" : f"{user_exists.get_session_token()}", "expires" : { "in" : 3600 , "units" : "seconds"}, "meta" : api_docs }
      else: 
        return {"message" : "Invalid credentials.", "meta" : api_docs}
    else:
      return {"message" : f"{email} could not be found. If you need to register, check the docs." , "meta" : api_docs}  


class UserRefreshToken(Resource):
  ''' /refresh '''

  @jwt_required
  def post(self):
    token = User.get_request_token(request)
    user = User.verify_session_token(token)
    if not user:
      return {"message": "Invalid or expired token. You need to re-authenticate.", "meta" : api_docs}, 401
    return {"logged in as": f"{user.username} {user.email}", "message" : "Success.", "token" : f"{user.get_session_token()}", "expires" : { "in" : 3600 , "units" : "seconds"}, "meta" : api_docs}


class UserLogout(Resource):
  ''' /logout '''
  @jwt_required
  def post(self):
    token = User.get_request_token(request)
    user = User.verify_session_token(token)
    if not user:
      return {"message": "Invalid or expired token. You need to re-authenticate.", "meta" : api_docs}, 401
    user.delete_token()
    return {"message" : "Success. You have now logged out. Your token is now invalidated.", "meta" : api_docs}
      

class Todos(Resource):
  ''' /todos '''

  @jwt_required
  def get(self):
    token = User.get_request_token(request)
    user = User.verify_session_token(token)
    if not user:
      return {"message": "Invalid or expired token. You need to re-authenticate.", "meta" : api_docs}, 401
    todos_array = [{"id" : td.id, "status": td.status , "body" : td.body, "created" : f"{td.created_at}", "owner" : td.user.username} for td in user.get_todos()]
    return {"logged in as": f"{user.username} {user.email}", "todos" : todos_array , "total": len(todos_array), "meta" : api_docs}, 200

  @jwt_required
  def delete(self):
    token = User.get_request_token(request)
    user = User.verify_session_token(token)
    if not user:
      return {"message": "Invalid or expired token. You need to re-authenticate.", "meta" : api_docs}, 401
    user.delete_all_todos()
    return {"logged in as": f"{user.username} {user.email}", "message": "Success. All todos deleted.", "meta" : api_docs}, 200
    
  @jwt_required
  def post(self):
    token = User.get_request_token(request)
    user = User.verify_session_token(token)
    if not user:
      return {"message": "Invalid or expired token. You need to re-authenticate.", "meta" : api_docs}, 401
    data = parser.parse_args()
    body = data['body']
    status = data['status']
    new_todo = TodoModel.create_new(body=body, creator_id=user.id, status=status)
    return {"logged in as": f"{user.username} {user.email}", "message":"Success. Todo created.", "todo": { "id" : new_todo.id, "body": new_todo.body, "status":new_todo.status, "owner":new_todo.user.username , "created": f"{new_todo.created_at}" }, "meta" : api_docs}, 201


class Todo(Resource):
  ''' /todo/<todo_id> '''
  @jwt_required
  def get(self, todo_id):
    token = User.get_request_token(request)
    user = User.verify_session_token(token)
    if not user:
      return {"message": "Invalid or expired token. You need to re-authenticate.", "meta" : api_docs}, 401
    todo = user.get_todo(todo_id=todo_id)
    if not todo:
      return {"message": f"Could not find todo with an id of '{todo_id}'."}, 404
    todo_details = {"id" : todo.id, "status": todo.status , "body" : todo.body, "created" : f"{todo.created_at}", "owner" : todo.user.username}
    return {"logged in as": f"{user.username} {user.email}", "message" : "Success." , "todo" : todo_details, "meta" : api_docs}, 200

  @jwt_required
  def delete(self, todo_id):
    token = User.get_request_token(request)
    user = User.verify_session_token(token)
    if not user:
      return {"message": "Invalid or expired token. You need to re-authenticate.", "meta" : api_docs}, 401
    todo = user.get_todo(todo_id=todo_id)
    if not todo:
      return {"message": f"Could not find todo with an id of '{todo_id}'.", "meta" : api_docs}, 404
    user.delete_todo(todo_id)
    return {"logged in as": f"{user.username} {user.email}", "message": f"Success. Todo id {todo_id} deleted.", "meta" : api_docs}, 200

  @jwt_required
  def put(self, todo_id):
    token = User.get_request_token(request)
    user = User.verify_session_token(token)
    data = parser.parse_args()
    new_status = data['status']
    if not new_status:
      return {"message": "Missing updated status for todo.", "meta" : api_docs}, 400
    if not user:
      return {"message": "Invalid or expired token. You need to re-authenticate.", "meta" : api_docs}, 401
    todo = user.get_todo(todo_id=todo_id)
    if not todo:
      return {"message": f"Could not find todo with an id of '{todo_id}'.", "meta" : api_docs}, 404
    td = user.update_todo(todo_id=todo_id, new_status=new_status)
    return {"message" : "Success.", "todo" : {"id" : td.id, "status": td.status , "body" : td.body, "created" : f"{td.created_at}", "owner" : td.user.username }, "meta" : api_docs}

 
    