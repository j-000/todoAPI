from flask import render_template
from flask_restful import Api, reqparse
from flask_jwt_extended import JWTManager
from models import app
from resources import UserAuthentication, UserRefreshToken, UserRegistration, UserLogout, Todo


api = Api(app)
jwt = JWTManager(app)
api.add_resource(UserRegistration, '/registration')
api.add_resource(UserAuthentication, '/authentication')
api.add_resource(UserRefreshToken, '/refresh')
api.add_resource(UserLogout, '/logout')
api.add_resource(Todo, '/todos')


@app.route('/', methods=['GET', 'POST'])
def index():
  return render_template('index.html')

@app.route('/docs', methods=['GET'])
def documentation():
  return render_template('index.html')


# Start app
if __name__ == '__main__':
  app.run(debug=True)