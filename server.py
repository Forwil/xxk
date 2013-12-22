import web
import MySQLdb
import hashlib


urls = (
    '/', 'index',
    '/search','search',
    '/signup','signup',
	'/new','new'
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

def new_book(book):
	sql = "insert into book value(null,'%s','%s','%s','%s',0);"%(book["name"],book["author"],book["country"],book["language"])
	print sql		
	cur = conn.cursor()	
	cur.execute(sql)
	conn.commit()
	cur.close()
	return 

def new_moive(moive):
	sql = "insert into moive value(null,'%s','%s','%s','%s','%s','%s','%s',0);"%(moive["name"],moive["director"],moive["date"],moive["language"],moive["length"],moive["actor"],moive["abstract"])
	print sql		
	cur = conn.cursor()	
	cur.execute(sql)
	conn.commit()
	cur.close()
	return 

def new_music(music):
	sql = "insert into music value(null,'%s','%s','%s','%s',0);"%(music["name"],music["singer"],music["lrc"],music["rhythm"])
	print sql		
	cur = conn.cursor()	
	cur.execute(sql)
	conn.commit()
	cur.close()
	return 

def login(name,token):
	web.setcookie('name',name,3600)
	web.setcookie('token',token,3600)
	return 

def login_admin(name,token):
	web.setcookie('name',name,3600)
	web.setcookie('token',token,3600)
	web.setcookie('admin',"1",3600)
	return 

def logout():
	web.setcookie('name',"",-1)
	web.setcookie('token',"",-1)	
	web.setcookie('admin',"",-1)	
	return

def find_user(email):
	sql = "select * from user where email='%s'"	%(email)
	cur = conn.cursor()
	cur.execute(sql)
	conn.commit()
	result =cur.fetchone()
	cur.close()
	return result

def find_admin(email):
	sql = "select * from admin where email='%s'" %(email)
	cur = conn.cursor()
	cur.execute(sql)
	conn.commit()
	result =cur.fetchone()
	cur.close()
	return result

def my_page(f):
	user = web.cookies().get("name","")
	token = web.cookies().get("token","")
	return render.layout(render.header(user,token),f())

class new:
	def GET(self):
		i = web.input()
		t = i.get("type","")
		if t == "3":
			return my_page(render.newbook)
		elif t == "2":
			return my_page(render.newmoive)
		else:
			return my_page(render.newmusic)
	def POST(self):
		i = web.input()
		if i["type"] == "3":
			new_book(i)
		elif i["type"] == "2":
			new_moive(i)
		else:
			new_music(i)
		return i

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
		if web.cookies().get("admin","") != "":
			return my_page(render.admin)
		return my_page(render.index)
	def POST(self):
		i = web.input()
		if "admin" in i:
			tmp = find_admin(i["email"])
			if (tmp != None and tmp[3] == i['passwd']):
				login_admin(tmp[1],tmp[4])	
		else:
			tmp = find_user(i["email"])
			if (tmp != None and tmp[3] == i['passwd']):
				login(tmp[1],tmp[8])
		web.seeother("/")

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
