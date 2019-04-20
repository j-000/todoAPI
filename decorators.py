from functools import wraps
from flask import request

''' decorator function to ensure all protected API endpoints have a jwt in the authorization header.
    THIS DECORATOR DOES NOT VALIDATE THE JWT TOKEN
 '''
def jwt_required(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
      return {"message": "No authorization header defined."}
    try:
      auth_token = auth_header.split()[1]
    except:
      return {"message": "No token found in authorization header."}
    return f(*args, **kwargs)
  return wrapper
