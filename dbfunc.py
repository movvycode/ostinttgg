from peewee import *
db = SqliteDatabase("data.db")

class User(Model):
    num_id = IntegerField(primary_key=True)
    tg_id = IntegerField(unique=True)
    
    class Meta:
        database = db

def create_db():
	try:
		db.create_tables([User])
	except IntegrityError:
		pass
def add_admins():
	try:
		dev = User.create(tg_id=1056861593)
		dev.save()
	except IntegrityError:
		pass

def add_db_user(user_id: int):
	try:
		user = User.create(tg_id=user_id)
		user.save()
	except IntegrityError:
		pass

def stats():
	s = []
	q = User.select(User.tg_id)
	for user in q:
		s.append(user.tg_id)
	return f'<b>💥 Пользователей в боте: {len(s)}</b>'
def getall():
	s = []
	q = User.select(User.tg_id)
	for user in q:
		s.append(user.tg_id)
	return s
	s.clear()