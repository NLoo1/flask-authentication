from app.app import app
from app.models import db, User

with app.app_context():
    db.drop_all()
    db.create_all()

    user = User.register(username="Test1", password="password", email="test-email@gmail.com", first_name="John", last_name="Doe")
    user2 = User.register(username="Test2", password="abc123", email="test-email@hotmail.com", first_name="Jane", last_name="Doe")
    user3 = User.register(username="Test3", password="baseball", email="test-email@yahoo.com", first_name="Jimmy", last_name="Neutron")

    db.session.add_all([user,user2,user3])
    db.session.commit()