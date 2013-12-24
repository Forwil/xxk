#encoding=utf-8
import web
import sys
import MySQLdb
import hashlib
import time
import MySQLdb.cursors

reload(sys)
sys.setdefaultencoding('utf-8')

urls = (
    '/', 'index',
    '/search','search',
    '/signup','signup',
	'/new','new',
	'/music','music',
	'/moive','moive',
	'/book','book',
	'/delete','delete',
	'/edit','edit',
	'/user','user'
)

render = web.template.render('templates/')

conn = MySQLdb.connect(
host='localhost',
user='root',
passwd='19921229',
db='xxk',
port=3306,
charset='utf8',
cursorclass = MySQLdb.cursors.DictCursor
)

def get_token(s):
	return hashlib.md5(s).hexdigest()

def run_sql(sql):
	print sql
	cur = conn.cursor()	
	cur.execute(sql)
	conn.commit()
	cur.close()

def get_one_sql(sql):
	print sql
	cur = conn.cursor()	
	cur.execute(sql)
	result =cur.fetchone()
	conn.commit()
	cur.close()
	return result

def get_all_sql(sql):	
	print sql
	cur = conn.cursor()	
	cur.execute(sql)
	result =cur.fetchall()
	conn.commit()
	cur.close()
	return result

def new_user(user):
	token = get_token(user["email"])
	sql = "insert into user value(null,'%s','%s','%s','%s','%s','%s','%s','%s');"%(user['name'],user['email'],user['passwd'],user['gender'],user['birth'],user['school'],user['major'],token)
	run_sql(sql)
	return user['name'],token

def edit_user(user):
	sql = "update user set name='%s',email='%s',passwd='%s',gender='%s',birth='%s',school='%s',major='%s' where id=%s;"%(user['name'],user['email'],user['passwd'],user['gender'],user['birth'],user['school'],user['major'],user['id'])
	run_sql(sql)
	return 


def new_manage(admin_id,typ,item_id):
	sql = "insert into manage value('%s','%s','%s');" % (admin_id,item_id,typ)
	run_sql(sql)
	return 

def get_now_id(user):
	token = web.cookies().get("token","") 
	sql = "select * from %s where token='%s';" %(user,token)
	result = get_one_sql(sql)
	if result == None:
		return None
	else:
		return result['id']

def get_max_id(typ):
	sql = "select MAX(id) from %s;" %(typ)
	res = get_one_sql(sql)
	return res['MAX(id)']

def new_book(book):
	sql = "insert into book value(null,'%s','%s','%s','%s','%s',0);"%(book["url"],book["name"],book["author"],book["country"],book["language"])
	run_sql(sql)
	return 

def edit_book(book):
	sql = "update book set url='%s',name='%s',author='%s',country='%s',language='%s' where id='%s';"%(book["url"],book["name"],book["author"],book["country"],book["language"],book['id'])
	run_sql(sql)
	return 

def new_moive(moive):
	sql = "insert into moive value(null,'%s','%s','%s','%s','%s','%s','%s','%s',0);"%(moive["url"],moive["name"],moive["director"],moive["date"],moive["language"],moive["length"],moive["actor"],moive["abstract"])
	run_sql(sql)
	return 

def edit_moive(moive):
	sql = "update moive set url='%s',name='%s',director='%s',date='%s',language='%s',length='%s',actor='%s',abstract='%s' where id='%s';"%(moive["url"],moive["name"],moive["director"],moive["date"],moive["language"],moive["length"],moive["actor"],moive["abstract"],moive['id'])
	run_sql(sql)
	return

def new_music(music):
	sql = "insert into music value(null,'%s','%s','%s','%s','%s',0);"%(music["url"],music["name"],music["singer"],music["lrc"],music["rhythm"])
	run_sql(sql)
	return 

def edit_music(music):
	sql = "update music set url='%s',name='%s',singer='%s',lrc='%s',rhythm='%s' where id='%s';"%(music["url"],music["name"],music["singer"],music["lrc"],music["rhythm"],music['id'])
	run_sql(sql)
	return 

def new_comment(user_id,item_id,typ,content):
	t = time.strftime("%Y-%m-%d %H:%M:%S")
	sql = "insert into comment value('%s','%s','%s','%s','%s',null);" % (user_id,item_id,typ,content,t)
	run_sql(sql)
	sql = "update %s set comments_num = comments_num + 1 where id=%s;" %(typ,item_id)
	run_sql(sql)
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

def find_user_by_email(email):
	sql = "select * from user where email='%s';" %(email)
	result = get_one_sql(sql)
	return result

def find_admin_by_email(email):
	sql = "select * from admin where email='%s';" %(email)
	result =get_one_sql(sql)
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
	return get_all_sql(sql)

def find_by_id(typ,id):
	sql = "select * from %s where id=%s;"%(typ,id)
	return get_one_sql(sql)

def find_comments(typ,id):
	sql = "select * from comment where type='%s' and item_id=%s order by time;" % (typ,id)	
	result = get_all_sql(sql)
	resdis = []
	for i in range(0,len(result)):
		resdis.append({})
		resdis[i]["name"] = find_by_id("user",result[i]["user_id"])["name"]
		resdis[i]["content"] = result[i]["content"]
		resdis[i]["time"] = result[i]["time"]
		if web.cookies().get("name","") == resdis[i]["name"]:
			resdis[i]["del"] = 1
		else:
			resdis[i]["del"] = 0
		resdis[i]["id"] = result[i]["user_id"]
	return resdis

def drop(typ,id):
	if typ=="comment":
		a = find_by_id(typ,id)
		sql = "update %s set comments_num = comments_num-1 where id=%s;"%(a["type"],a["id"])
		run_sql(sql)
	sql = "delete from %s where id=%s;"%(typ,id)
	run_sql(sql)
	return

def find_admin(typ,id):
	sql = "select * from manage where item_id=%s and type='%s';"%(id,typ)
	result = get_one_sql(sql)
	if result == None:
		return None
	else:
		return result['admin_id']		

def render_one(i,typ):
	result = find_by_id(typ,i["id"])
	comm = find_comments(typ,i["id"])
	ad = find_admin(typ,i["id"])
	flag = not(None == web.cookies().get("admin",None) or get_now_id("admin")!= ad)
	return my_page(render.one(result,render.comments(comm),flag,typ))

def render_list(typ):
	return my_page(render.list(typ,find_by_name(typ,"")))

def new_some(i,typ):
	if web.cookies().get("admin","")!="" or web.cookies().get("name","")=="":
		web.seeother("/%s?id=%s" % (typ,i["id"]))
		return 
	new_comment(get_now_id("user"),i["id"],typ,i["content"])
	web.seeother("/%s?id=%s" % (typ,i["id"]))

class delete:
	def GET(self):
		i = web.input()
		drop(i["type"],i["id"])
		return '<script language="javascript">window.location.href = "http://localhost:8080/"</script>'

class music:
	def GET(self):
		i = web.input()
		if "id" in i:
			return render_one(i,"music")
		return render_list("music")
	def POST(self):
		i = web.input()
		new_some(i,"music")

class moive:
	def GET(self):
		i = web.input()
		if "id" in i:
			return render_one(i,"moive")
		return render_list("moive")
	def POST(self):
		i = web.input()
		new_some(i,"moive")

class book:
	def GET(self):
		i = web.input()
		if "id" in i:
			return render_one(i,"book")
		return render_list("book")
	def POST(self):
		i = web.input()
		new_some(i,"book")

class edit:
	def GET(self):
		i = web.input()
		t = i.get("type","")
		one = find_by_id(t,i['id'])
		if t == "book":
			return my_page(render.editbook(one))
		elif t == "moive":
			return my_page(render.editmoive(one))
		elif t == "music":
			return my_page(render.editmusic(one))
		elif t == "user":
			return my_page(render.edituser(one))
	def POST(self):
		i = web.input()
		if i["type"] == "book":
			edit_book(i)
		if i["type"] == "moive":
			edit_moive(i)
		if i["type"] == "music":
			edit_music(i)
		if i["type"] == "user":
			edit_user(i)	
		web.seeother("/%s"% (i["type"]))

class new:
	def GET(self):
		i = web.input()
		t = i.get("type","")
		if t == "book":
			return my_page(render.newbook())
		elif t == "moive":
			return my_page(render.newmoive())
		elif t == "music":
			return my_page(render.newmusic())
	def POST(self):
		i = web.input()
		if i["type"] == "book":
			new_book(i)
		if i["type"] == "moive":
			new_moive(i)
		if i["type"] == "music":
			new_music(i)
		new_manage(get_now_id("admin"),i["type"],get_max_id(i["type"]))
		web.seeother("/" + i["type"])

class signup:
	def GET(self):
		return my_page(render.signup())

	def POST(self):
		i = web.input()
		if find_user_by_email(i["email"]) != None:
			web.seeother("/signup")
		else:
			login(*new_user(i))
			web.seeother("/")

class user:
	def GET(self):
		i = web.input()
		if i.get("id","")=="":
			return my_page(render.users(find_by_name("user","")))
		else:
			if web.cookies().get("admin","")=="":
				if i['id'] == str(get_now_id("user")):
					flag = True
				else:
					flag = False
			else:
				flag = False
			return my_page(render.user(find_by_id("user",i['id']),flag))

	def POST(self):
		return 

class search:
	def POST(self):
		i = web.input()
		if i['type'] == "book":
			return my_page(render.books(find_by_name("book",i["name"])))
		elif i['type'] == "moive":
			return my_page(render.moives(find_by_name("moive",i["name"])))
		elif i['type'] == "music":
			return my_page(render.musics(find_by_name("music",i["name"])))

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
			tmp = find_admin_by_email(i["email"])
		else:
			tmp = find_user_by_email(i["email"])
		if (tmp != None and tmp["passwd"] == i['passwd']):
			if "admin" in i:
				login_admin(tmp["name"],tmp["token"])
			else:	
				login(tmp["name"],tmp["token"])
		web.seeother("/")

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
