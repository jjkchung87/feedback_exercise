from unittest import TestCase
from app import app
from models import db, User, Feedback

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_exercise_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):			
    def setUp(self):
        Feedback.query.delete()
        User.query.delete()
     
        user = User.registration(username='AChung', password='arlo123', email='arlo@dog.com', first_name='Arlo', last_name='Chung')
        feedback = Feedback(title='Need more snacks', content='There is a serious shortage of snacks', username='AChung')
        
        self.user = user
        self.feedback = feedback

        db.session.add_all([user, feedback])
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
    
    # def testListOfUsers(self):
    #     with app.test_client() as client:
    #         resp = client.get('/users')
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn('', html )
    #         self.assertIn('Mcilroy', html )

    def testLogin(self):
        with app.test_client() as client:
            d = {'username': 'AChung',
                'password' : 'arlo123'}
            resp = client.post('/login', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            # self.assertIn('<h1 class="display1">User: AChung</h1>', html)
            self.assertEqual(resp.status_code, 200)

    def testRegister(self):
        with app.test_client() as client:
            d = {
                'username': 'TWoods',
                'password': 'tiger123',
                'first_name': 'Tiger',
                'last_name': 'Woods',
                'email': 'tiger@golf.com'
            }
            resp = client.post('/register', data=d, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="display1">User: TWoods</h1>', html)
            assert resp.request.path == '/register'

    def testUnauthorizedAddFeedback(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['username'] = 'MScott'
            resp = client.get(f'/users/{self.user.username}/feedback/add')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 401)
            self.assertIn("Not authenticated or authorized", html)

    def testUnauthorizedDeleteUser(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['username'] = 'MScott'
            resp = client.post(f'/users/{self.user.username}/delete')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 401)
            self.assertIn("Not authenticated or authorized", html)
    
    def testUnauthorizedDeleteFeedback(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['username'] = 'MScott'
            resp = client.post(f'/feedback/{self.feedback.id}/delete')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 401)
            self.assertIn("Not authenticated or authorized", html)
