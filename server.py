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
	'/book','book',
	'/delete','delete'
)

render = web.template.render('templates/')

conn = MySQLdb.connect(host='localhost',user='root',passwd='19921229',db='xxk',port=3306,charset='utf8')

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

def new_manage(admin_id,typ,item_id):
	sql = "insert into manage value('%s','%s','%s');" % (admin_id,item_id,typ)
	run_sql(sql)
	return 

def new_book(book):
	sql = "insert into book value(null,'%s','%s','%s','%s','%s',0);"%(book["url"],book["name"],book["author"],book["country"],book["language"])
	run_sql(sql)
	return 

def get_now_id(user):
	token = web.cookies().get("token","") 
	sql = "select * from %s where token='%s';" %(user,token)
	result = get_one_sql(sql)
	if result == None:
		return None
	else:
		return result[0]

def get_max_id(typ):
	sql = "select MAX(id) from %s;" %(typ)
	res = get_one_sql(sql)
	return res[0]

def new_moive(moive):
	sql = "insert into moive value(null,'%s','%s','%s','%s','%s','%s','%s','%s',0);"%(moive["url"],moive["name"],moive["director"],moive["date"],moive["language"],moive["length"],moive["actor"],moive["abstract"])
	run_sql(sql)
	return 

def new_music(music):
	sql = "insert into music value(null,'%s','%s','%s','%s','%s',0);"%(music["url"],music["name"],music["singer"],music["lrc"],music["rhythm"])
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
		resdis[i]["name"] = find_by_id("user",str(result[i][0]))[1]
		resdis[i]["content"] = result[i][3]
		resdis[i]["date"] = result[i][4]
		if web.cookies().get("name","") == resdis[i]["name"]:
			resdis[i]["del"] = 1
		else:
			resdis[i]["del"] = 0
		resdis[i]["id"] = result[i][5]
	return resdis

def drop(typ,id):
	if typ=="comment":
		a = find_by_id(typ,id)
		sql = "update %s set comments_num = comments_num-1 where id=%s;"%(a[2],a[1])
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
		return result[0]		

def render_one(i,typ):
	result = find_by_id(typ,i["id"])
	comm = find_comments(typ,i["id"])
	ad = find_admin(typ,i["id"])
	if ad == None or "" == web.cookies().get("admin",None) or get_user_id("admin")!= ad:
		flag = 0
	else:
		flag = 1
	if typ == "music":
		return my_page(render.music(result,render.comments(comm),flag))
	if typ == "moive":
		return my_page(render.moive(result,render.comments(comm),flag))
	if typ == "book":
		return my_page(render.book(result,render.comments(comm),flag))

def render_list(typ):
	if typ=="music":
		return my_page(render.musics(find_by_name(typ,"")))
	if typ=="moive":
		return my_page(render.moives(find_by_name(typ,"")))
	if typ=="book":
		return my_page(render.books(find_by_name(typ,"")))

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
			return render_one("music")
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
		new_manage(get_user_id("admin"),i["type"],get_max_id(i["type"]))
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
			if (tmp != None and tmp[3] == i['passwd']):
				login_admin(tmp[1],tmp[4])	
		else:
			tmp = find_user_by_email(i["email"])
			if (tmp != None and tmp[3] == i['passwd']):
				login(tmp[1],tmp[8])
		web.seeother("/")

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
