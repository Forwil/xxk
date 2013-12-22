#encoding=utf-8
import web
import sys
import MySQLdb
import hashlib
import time

reload(sys)
sys.setdefaultencoding('utf-8')

urls = (
    '/', 'index',
    '/search','search',
    '/signup','signup',
	'/new','new',
	'/music','music',
	'/moive','moive',
	'/book','book'
)

render = web.template.render('templates/')

conn = MySQLdb.connect(host='localhost',user='root',passwd='19921229',db='xxk',port=3306,charset='utf8')

def get_token(s):
	return hashlib.md5(s).hexdigest()

def is_exist_user(email):
	return False

def new_user(user):
	token = get_token(user["email"])
	sql = "insert into user value(null,'%s','%s','%s','%s','%s','%s','%s','%s');"%(user['name'],user['email'],user['passwd'],user['gender'],user['birth'],user['school'],user['major'],token)
	print sql
	cur = conn.cursor()	
	cur.execute(sql)
	conn.commit()
	cur.close()
	return user['name'],token

def new_book(book):
	sql = "insert into book value(null,'%s','%s','%s','%s','%s',0);"%(book["url"],book["name"],book["author"],book["country"],book["language"])
	print sql		
	cur = conn.cursor()	
	cur.execute(sql)
	conn.commit()
	cur.close()
	return 

def get_now_id():
	token = web.cookies().get("token","") 
	sql = "select * from user where token='%s';" %(token)
	print sql		
	cur = conn.cursor()	
	cur.execute(sql)
	result =cur.fetchone()
	conn.commit()
	cur.close()
	if result == None:
		return None
	else:
		return result[0]


def new_moive(moive):
	sql = "insert into moive value(null,'%s','%s','%s','%s','%s','%s','%s','%s',0);"%(moive["url"],moive["name"],moive["director"],moive["date"],moive["language"],moive["length"],moive["actor"],moive["abstract"])
	print sql		
	cur = conn.cursor()	
	cur.execute(sql)
	conn.commit()
	cur.close()
	return 

def new_music(music):
	sql = "insert into music value(null,'%s','%s','%s','%s','%s',0);"%(music["url"],music["name"],music["singer"],music["lrc"],music["rhythm"])
	print sql		
	cur = conn.cursor()	
	cur.execute(sql)
	conn.commit()
	cur.close()
	return 

def new_comment(user_id,item_id,typ,content):
	t = time.strftime("%Y-%m-%d %H:%M:%S")
	sql = "insert into comment value('%s','%s','%s','%s','%s');" % (user_id,item_id,typ,content,t)
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
	login(name,token)
	web.setcookie('admin',"1",3600)
	return 

def logout():
	web.setcookie('name',"",-1)
	web.setcookie('token',"",-1)	
	web.setcookie('admin',"",-1)	
	return

def find_user(email):
	sql = "select * from user where email='%s';" %(email)
	cur = conn.cursor()
	cur.execute(sql)
	conn.commit()
	result =cur.fetchone()
	cur.close()
	return result

def find_admin(email):
	sql = "select * from admin where email='%s';" %(email)
	cur = conn.cursor()
	cur.execute(sql)
	conn.commit()
	result =cur.fetchone()
	cur.close()
	return result

def my_page(body):
	user = web.cookies().get("name","")
	token = web.cookies().get("token","")
	return render.layout(render.header(user,token),body)

def find_by_name(typ,name):
	if name=="":
		sql = "select * from %s;"%(typ)
	else:
		sql = "select * from %s where name='%s';" %(typ,name)
	print sql
	cur = conn.cursor()
	cur.execute(sql)
	result = []
	while True:
		t = cur.fetchone()
		if t!=None:
			result.append(t)
		else:
			break
	conn.commit()
	cur.close()
	return result

def find_by_id(typ,id):
	sql = "select * from %s where id=%s;"%(typ,id)
	print sql
	cur = conn.cursor()
	cur.execute(sql)
	result = cur.fetchone()
	conn.commit()
	cur.close()
	return result

def find_music(name):
	return find_by_name("music",name)

def find_moive(name):
	return find_by_name("moive",name)

def find_book(name):
	return find_by_name("book",name)

def find_comments(typ,id):
	sql = "select * from comment where type='%s' and item_id=%s order by time;" % (typ,id)	
	print sql
	cur = conn.cursor()
	cur.execute(sql)
	result = []
	while True:
		t = cur.fetchone()
		if t!=None:
			result.append(t)
		else:
			break
	resdis = []
	for i in range(0,len(result)):
		resdis.append({})
		resdis[i]["name"] = find_by_id("user",str(result[i][0]))[1]
		resdis[i]["content"] = result[i][3]
		resdis[i]["date"] = result[i][4]
	print resdis
	conn.commit()
	cur.close()
	return resdis

class music:
	def GET(self):
		i = web.input()
		if "id" in i:
			result = find_by_id("music",i["id"])
			comm = find_comments("music",i["id"])
			return my_page(render.music(result,render.comments(comm)))
		return my_page(render.musics(find_music("")))
	def POST(self):
		i = web.input()
		nowid = get_now_id()
		new_comment(nowid,i["id"],"music",i["content"])
		web.seeother("/music?id=%s" % (i["id"]))

class moive:
	def GET(self):
		i = web.input()
		if "id" in i:
			result = find_by_id("moive",i["id"])
			comm = find_comments("moive",i["id"])
			return my_page(render.book(result,render.comments(comm)))
		return my_page(render.moives(find_moive("")))

	def POST(self):
		i = web.input()
		nowid = get_now_id()
		new_comment(nowid,i["id"],"moive",i["content"])
		web.seeother("/moive?id=%s" % (i["id"]))

class book:
	def GET(self):
		i = web.input()
		if "id" in i:
			result = find_by_id("book",i["id"])
			comm = find_comments("book",i["id"])
			return my_page(render.book(result,render.comments(comm)))
		return my_page(render.books(find_book("")))
	def POST(self):
		i = web.input()
		nowid = get_now_id()
		new_comment(nowid,i["id"],"book",i["content"])
		web.seeother("/book?id=%s" % (i["id"]))

class new:
	def GET(self):
		i = web.input()
		t = i.get("type","")
		if t == "3":
			return my_page(render.newbook())
		elif t == "2":
			return my_page(render.newmoive())
		else:
			return my_page(render.newmusic())
	def POST(self):
		i = web.input()
		if i["type"] == "3":
			new_book(i)
			web.seeother("/book")
		elif i["type"] == "2":
			new_moive(i)
			web.seeother("/moive")
		else:
			new_music(i)
			web.seeother("/music")

class signup:
	def GET(self):
		return my_page(render.signup())

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
		if i['type'] == "3":
			return my_page(render.books(find_book(i["name"])))
		elif i['type'] == "2":
			return my_page(render.moives(find_moive(i["name"])))
		else:
			return my_page(render.musics(find_music(i["name"])))

class index:
	def GET(self):
		i = web.input()
		if "logout" in i:
			logout()
			web.seeother("/")
		if web.cookies().get("admin","") != "":
			return my_page(render.admin())
		return my_page(render.index())
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
