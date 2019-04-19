from models import db, User

def start_db():
  db.drop_all()
  db.create_all()

def create_user():
  new_user = User.create_new(username='joao', email='j@j.j', password='tina123')


if __name__ == "__main__":
  start_db()
  create_user()