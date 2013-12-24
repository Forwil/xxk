import MySQLdb

conn = MySQLdb.connect(host='localhost',user='root',passwd='19921229',db='xxk',port=3306,charset='utf8')

def new_user(user):
	token = get_token(user["email"])
	sql = "insert into user value(null,'%s','%s','%s','%s','%s','%s','%s','%s');"%(user['name'],user['email'],user['passwd'],user['gender'],user['birth'],user['school'],user['major'],token)
	print sql
	cur = conn.cursor()	
	cur.execute(sql)
	conn.commit()
	cur.close()
	return user['name'],token

def new_manage(admin_id,typ,item_id):
	sql = "insert into manage value('%s','%s','%s');" % (admin_id,item_id,typ)
	print sql		
	cur = conn.cursor()	
	cur.execute(sql)
	conn.commit()
	cur.close()
	return 

def new_book(book):
	sql = "insert into book value(null,'%s','%s','%s','%s','%s',0);"%(book["url"],book["name"],book["author"],book["country"],book["language"])
	print sql		
	cur = conn.cursor()	
	cur.execute(sql)
	conn.commit()
	cur.close()
	return 

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



