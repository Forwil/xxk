import web
import MySQLdb
import hashlib


urls = (
    '/', 'index',
    '/search','search',
    '/signup','signup'
)

render = web.template.render('templates/')

conn = MySQLdb.connect(host='localhost',user='root',passwd='19921229',db='xxk',port=3306)

def get_token(s):
	return hashlib.md5(s).hexdigest()

def is_exist_user(email):
	return False

def new_user(user):
	token = get_token(user["email"])
	sql = "insert into user value(null,'%s','%s','%s','%s','%s','%s','%s','%s');"%(user['name'],user['email'],user['passwd'],user['gender'],user['birth'],user['school'],user['major'],token)
	cur = conn.cursor()	
	cur.execute(sql)
	conn.commit()
	cur.close()
	return user['name'],token

def login(name,token):
	web.setcookie('name', name, 3600)
	web.setcookie('token',token,3600)
	return 

def logout():
	web.setcookie('name',"",-1)
	web.setcookie('token',"",-1)	
	return

def find_user(email):
	sql = "select * from user where email='%s'"	%(email)
	cur = conn.cursor()
	cur.execute(sql)
	conn.commit()
	result =cur.fetchone()
	cur.close()
	return result

def my_page(f):
	user = web.cookies().get("name","")
	return f(render.header(user))

class signup:
	def GET(self):
		return my_page(render.signup)

	def POST(self):
		i = web.input()
		if find_user(i["email"]) != None:
			web.seeother("/signup")
		else:
			login(*new_user(i))
			web.seeother("/")

class search:
	def POST(self):
		i = web.input()
		print i
		return i

class index:
	def GET(self):
		i = web.input()
		if "logout" in i:
			logout()
			web.seeother("/")
		return my_page(render.index)
	def POST(self):
		i = web.input()
		tmp = find_user(i["email"])
		if (tmp != None and tmp[3] == i['passwd']):
			login(tmp[1],tmp[8])
		web.seeother("/")

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
