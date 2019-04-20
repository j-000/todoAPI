from models import db, User, TodoModel

def start_db():
  db.drop_all()
  db.create_all()

def create_user():
  new_user = User.create_new(username='test', email='test@test.com', password='test')

def create_todos():
  todo1 = TodoModel.create_new("Wash the dishes!", 1, "Not done.")
  todo2 = TodoModel.create_new("Study for exam!", 1, "Not done.")

if __name__ == "__main__":
  start_db()
  create_user()
  create_todos()