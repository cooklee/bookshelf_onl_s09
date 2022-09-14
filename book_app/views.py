from django.shortcuts import render

from book_app.models import Author


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
                      {'message':f'Udało sie stworzyć autora {imie} {nazwisko}'})


def view_authors(request):
    last_name = request.GET.get('last_name', '')
    authors = Author.objects.filter(last_name__icontains=last_name)
    return render(request, 'view_authors.html', {'authors':authors})


def view_detail_author(request, author_id):
    author = Author.objects.get(id=author_id)
    return render(request, 'author.html', {'author':author})
