import os,sys
import datetime
import jinja2

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib.zip'))
from bottle import *
from ctl.model import *

from google.appengine.api import oauth

# create our own bottle object instead of relying on the default bottle object, 
# we will pass it to the WSGI app handler
app=Bottle() 
debug(True)

jinja_env = jinja2.Environment(\
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),\
	extensions=['jinja2.ext.autoescape'])

# attach all our routes and handlers to this bottle object
@app.route('/')
def get():
	t = jinja_env.get_template('/template/index.html')
	#ip = request.environ.get('REMOTE_ADDR')
	allTypeEntitys = articleType.all()
	allArticle = article.all()
	return t.render(warning="Hello Anonymous. This is my homepage. \
		It is under construction right now. It'll be a demo of my study.", \
					allArticles = allArticle, allTypes=allTypeEntitys)

@app.post('/lnote')
def lnote():
	return "Ooo ...  It's under construction. Welcome back soon."

@app.route('/postlist')
def postList():
	act = request.query.get("t")
	key = request.query.get("id")

	if act == None:
		t = jinja_env.get_template('/template/postlist.html')
		allTypeEntitys = articleType.all()
		allArticle = article.all()
		return t.render(allArticles = allArticle, allTypes=allTypeEntitys)
	elif act == 'del':
		do = articleDo()		
		do.dele(key)
		# how to refresh ???
		redirect("/postlist")
	else:
		pass

@app.route('/article/details/<id>')
def detail(id):
	t = jinja_env.get_template('/template/index.html')
	do = articleDo()
	article2Show = do.get(id)	
	return t.render(warning="Hello Anonymous. This is my homepage. \
		It is under construction right now.", article2Show=article2Show)

@app.route('/category')
def category():
	t = jinja_env.get_template('/template/category.html')
	allTypeEntitys = articleType.all()
	return t.render(allTypes = allTypeEntitys)

@app.post('/category/add')
def categoryAdd():
	type = articleType()
	type.typeName = request.forms.get("typeAdd")
	type.articleCount = 0
	type.put()
	redirect("/category")

@app.route('/feedback')
def feedback():
	pass

@app.route('/configure')
def configure():
	pass

@app.route('/draft')
def draft():
	pass

@app.route('/deleted')
def deleted():
	pass

@app.route('/postedit')
def postEdit():
	key = request.query.get("id")
	allTypeEntitys = articleType.all()
	t = jinja_env.get_template('/template/postedit.html')	
	if key == None:	
		return t.render(allTypes = allTypeEntitys)
	else:
		do = articleDo()
		articleEdit = do.get(key)			
		return t.render(title = articleEdit.title, content = articleEdit.content, \
			act = "/postedit/up?id="+key, allTypes = allTypeEntitys)

@app.post('/postedit/add')
def postAdd():

	newArticle = article()
	newArticle.title = request.forms.get("articleTitle")
	newArticle.content = request.forms.get("articleContent")
	newArticle.postime = datetime.today()
	newArticle.readCount = 0
	newArticle.commentCount = 0
	newArticle.put()
	# how to refresh ???
	redirect("/postlist")	

@app.post('/postedit/up')
def postAdd():
	key = request.query.get("id")
	do = articleDo()
	articleUp = do.get(key)
	articleUp.title = request.forms.get("articleTitle")
	articleUp.content = request.forms.get("articleContent")
	articleUp.put()
	# how to refresh ???
	redirect("/postlist")

@app.error(404)
def error404(error):
	return '404! (- Nothing here.'

@app.route("/login")
def login():
	t = jinja_env.get_template('/template/login.html')
	return t.render() 
