import web

urls = (
    '/', 'index',
    '/search','search',
    '/signup','signup'
)
render = web.template.render('templates/')

class signup:
	def GET(self):
		return render.signup("")
	def POST(self):
		i = web.input()
		return i 

class search:
	def POST(self):
		i = web.input()
		print i
		return i

class index:
	def GET(self):
		return render.index("")
	def POST(self):
		i = web.input()
		print i
		return render.index("Forwil")

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
