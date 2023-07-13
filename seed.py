"""Seed file to make sample data for db"""

from models import User, Feedback, db
from app import app
from sqlalchemy import text


#create all tables

db.drop_all()
db.create_all()

u1 = User.registration(username='AChung', password='arlo123', email='arlo@dog.com', first_name='Arlo', last_name='Chung')
u2 = User.registration(username='RMcilroy', password='rory123', email='rory@golfer.com', first_name='Rory', last_name='Mcilroy')
u3 = User.registration(username='MScott', password='michael123', email='michael@office.com', first_name='Michael', last_name='Scott')

f1 = Feedback(title='Need more snacks', content='There is a serious shortage of snacks', username='AChung')
f2 = Feedback(title='Need more walks', content='I need more walks. Getting too lazy', username='AChung')
f3 = Feedback(title='LIV needs to go', content='LIV is such a joke and is detracting away from the game. It needs to go!', username='RMcilroy')
f4 = Feedback(title='Patrick Reed needs to get a life!', content='What a loser. He needs to get a life and leave me alone.', username='RMcilroy')
f5 = Feedback(title='We need more excitement in the office', content='The office is not a place for work. It is a place to have fun.', username='MScott')
f6 = Feedback(title='My review of Bowling for Columbine', content='It was a good movie, but not a lot of bowling in it.', username='MScott')



db.session.add_all([u1,u2,u3,f1,f2,f3,f4,f5,f6])
db.session.commit()
