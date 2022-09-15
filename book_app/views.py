from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from book_app.models import Author, Book, Genre


# Create your views here.
def index(request):
    ln = request.session.get('lang', 'nie wybrano jezyka')
    ln_ciastko = request.COOKIES.get('lang', 'nie wybrano jezyka w ciasteczku')
    return render(request, "base.html", {'ln': ln, 'ln_c': ln_ciastko})


def add_author(request):
    if request.method == 'GET':
        return render(request, 'add_author.html')
    else:
        imie = request.POST['first_name']
        nazwisko = request.POST['last_name']
        Author(first_name=imie, last_name=nazwisko).save()
        return render(request, 'add_author.html',
                      {'message': f'Udało sie stworzyć autora {imie} {nazwisko}'})


def view_authors(request):
    last_name = request.GET.get('last_name', '')
    authors = Author.objects.filter(last_name__icontains=last_name)
    return render(request, 'view_authors.html', {'authors': authors})


def books(request):
    books = Book.objects.all()
    return render(request, 'books.html', {'ksiazki': books})


def view_detail_author(request, author_id):
    author = Author.objects.get(id=author_id)
    return render(request, 'author.html', {'author': author})


class AddBookView(View):

    def get(self, request):
        authors = Author.objects.all().order_by('last_name')
        genres = Genre.objects.order_by('name')
        return render(request, 'add_book.html', {'authors': authors,
                                                 'genres': genres})

    def post(self, request):
        title = request.POST['title']
        author_id = request.POST['author_id']
        author = Author.objects.get(id=author_id)
        b = Book(title=title, author=author)
        b.save()
        genres_ids = request.POST.getlist('genre')
        b.genres.set(genres_ids)
        return render(request, 'add_book.html', {'message': 'ksiazka dodana'})


class BookDetailView(View):

    def get(self, request, book_id):
        book = Book.objects.get(pk=book_id)
        return render(request, 'book.html', {'ksiazka': book})


class AddSessionView(View):

    def get(self, request):
        return render(request, 'lang.html')

    def post(self, request):
        ln = request.POST['lang']
        request.session['lang'] = ln

        return redirect('/')


def get(request):
    return render(request, 'lang.html')


class AddCookieView(View):

    def post(self, request):
        ln = request.POST['lang']
        http_response = redirect('/')
        http_response.set_cookie('lang', ln)

        return http_response


class CounterSetView(View):

    def get(self, request):
        x = 0
        request.session['counter'] = x
        return HttpResponse(f"counter uswawiłem na {x}")


class CounterShowView(View):

    def get(self, request):
        x = request.session.get('counter', 'ni ma')
        if type(x) is int:
            request.session['counter'] = x + 1
        return HttpResponse(f"wartosc counter = {x}")


class CounterDeleteView(View):

    def get(self, request):
        del request.session['counter']
        return HttpResponse(f"usunołem counter")


class Zad3Sessije(View):

    def get(self, request):
        return render(request, 'create_sesion.html', {'sessje': request.session})

    def post(self, request):
        key = request.POST['key']
        value = request.POST['value']
        request.session[key] = value
        return redirect("/add_zad3_session/")



class CookieSetView(View):

    def get(self, request):
        hr = HttpResponse("ustwiono cisteczko user")
        hr.set_cookie('user', 'sławek')
        return hr


class CookieShowView(View):

    def get(self, request):
        return HttpResponse(f"wartosc ciasteczka user to {request.COOKIE['user']}")


class CookieDeleteView(View):

    def get(self, request):
        hr = HttpResponse('usuwam ciasteczko USER')
        hr.delete_cookie('user')
        return hr


class Zad2Kukis(View):

    def get(self, request):
        return render(request, 'create_sesion.html', {'sessje': request.COOKIE})

    def post(self, request):
        key = request.POST['key']
        value = request.POST['value']
        hr = redirect("/add_zad3_session/")
        hr.set_cookie(key, value)
        return hr