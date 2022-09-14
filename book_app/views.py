from django.shortcuts import render
from django.views import View

from book_app.models import Author, Book, Genre


# Create your views here.
def index(request):
    return render(request, "base.html")


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
        return render(request, 'book.html', {'ksiazka':book})
