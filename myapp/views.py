from django.shortcuts import render, HttpResponse
 
topics = [
    {'id':1, 'title' : 'Routing', 'body' : 'Routing is ...'},
    {'id':2, 'title' : 'View', 'body' : 'View is ...'},
    {'id':3, 'title' : 'model', 'body' : 'Model is ...'}
]

def HTMLTemplete(articleTag):
    global topics
    ol = ''
    for topic in topics:
        ol += f'<li><a href ="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return f'''
    <html>
    <body>
        <h1><a href="/">Django</a></h1>
        <ol>
            {ol}
        </ol>
        {articleTag}
        <ul>
            <li><a href="/create/">create</a></li>
        </ul>
    </body>
    </html>
    '''

def index(req):
    article = '''
    <h2>Welcome</h2>
        Hello, Django
    '''
    return HttpResponse(HTMLTemplete(article))
    
def read(req, id):
    global topics
    article = ''
    for topic in topics:
        if topic['id'] == int(id):
            article =f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(HTMLTemplete(article))

def create(req):
    article = '''
        <form action="/create/">
            <p><input type="text" name="title" placeholder="title"></p>
            <p><textarea name="body" placeholder="body"></textarea></p>
            <p><input type="submit"></p>
        </form>
    '''
    return HttpResponse(HTMLTemplete(article))
