from app.app import app
from app.models import Feedback, db, User

with app.app_context():
    db.drop_all()
    db.create_all()

    user = User.register(username="Test1", pwd="password", email="test-email@gmail.com", first_name="John", last_name="Doe")
    user2 = User.register(username="Test2", pwd="abc123", email="test-email@hotmail.com", first_name="Jane", last_name="Doe")
    user3 = User.register(username="Test3", pwd="baseball", email="test-email@yahoo.com", first_name="Jimmy", last_name="Neutron")

    db.session.add_all([user,user2,user3])
    db.session.commit()

    feedback1 = Feedback(title='Test',content='TestContent',username='Test1')
    feedback2 = Feedback(title='Test2',content='TestContent2',username='Test2')
    feedback3 = Feedback(title='Test3',content='TestContent3',username='Test3')

    db.session.add_all([feedback1,feedback2,feedback3])
    db.session.commit()