from models import db, User, TodoModel

def start_db():
  db.drop_all()
  db.create_all()

def create_user():
  new_user = User.create_new(username='joao', email='j@j.j', password='tina123')

def create_todos():
  todo1 = TodoModel.create_new("Wash the dishes!", 1, "not done")
  todo2 = TodoModel.create_new("Study for exam!", 1, "not done")

if __name__ == "__main__":
  start_db()
  create_user()
  create_todos()