from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    print(request)
    return HttpResponse("<h1>Hello world!<h1>")

def test(request):
    return HttpResponse("<h1>test page<h1>")
def test1(requests):
    return HttpResponse("<h1>Test page1<h1>")
def test2(requests):
    return HttpResponse(
        """<html>
             <head>
             <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
             <title>Пример веб-страницы</title>
            </head>
            <body>
             <h1>Заголовок</h1>
             <!-- Комментарий -->
             <p>Первый абзац.</p>
             <p>Второй абзац.</p>
            </body>
           </html>""")

