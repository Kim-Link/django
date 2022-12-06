from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
 
nextId = 4
topics = [
    {'id':1, 'title' : 'Routing', 'body' : 'Routing is ...'},
    {'id':2, 'title' : 'View', 'body' : 'View is ...'},
    {'id':3, 'title' : 'model', 'body' : 'Model is ...'}
]

def HTMLTemplete(articleTag, id=None):
    global topics
    contextUI = ''
    if id != None:
        contextUI = f'''
            <li>
                <form action="/delete/" method="post">
                    <input type="hidden" name="id" value={id}>
                    <input type="submit" value="delete">
                </form>
            </li>
            <li><a href="/update/{id}">update</a></li>
        '''
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
            {contextUI}
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
    return HttpResponse(HTMLTemplete(article, id))

@csrf_exempt
def create(req):
    global nextId
    if req.method == 'GET':
        article = '''
            <form action="/create/" method="post">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(HTMLTemplete(article))
    elif req.method == 'POST':
        title = req.POST['title']
        body = req.POST['body']
        newTopic = {"id" : nextId,"title" : title, "body" : body}
        topics.append(newTopic)
        url = '/read/' + str(nextId)
        nextId = nextId + 1
        return redirect(url)

@csrf_exempt
def update(req, id):
    global topics
    if req.method == 'GET':
        for topic in topics:
            if topic['id'] == int(id):
                selectedTopic = {
                    "title":topic['title'],
                    "body":topic['body']
                }
        article = f'''
            <form action="/update/{id}/" method="post">
                <p><input type="text" name="title" placeholder="title" value={selectedTopic["title"]}></p>
                <p><textarea name="body" placeholder="body">{selectedTopic['body']}</textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(HTMLTemplete(article, id))
    elif req.method == 'POST':
        title = req.POST['title']
        body = req.POST['body']
        for topic in topics:
            if topic['id'] == int(id):
                topic['title'] = title
                topic['body'] = body
        return redirect(f'/read/{id}')

@csrf_exempt
def delete(req):
    global topics
    if req.method == 'POST':
        id = req.POST['id']
        newTopics = []
        for topic in topics:
            if topic['id'] != int(id):
                newTopics.append(topic)
        topics = newTopics
        return  redirect('/')
