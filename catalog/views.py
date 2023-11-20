from django.shortcuts import render
from catalog.models import Book, BookInstance, Genre, Author
from django.views import generic
from django.shortcuts import get_object_or_404

# Create your views here.


def index(request):
    """View function for home page of site"""

    # Generate counts of some of the main object

    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    num_instances_available = BookInstance.objects.filter(status="a").count()

    num_authors = Author.objects.count()

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
    }

    return render(request, "index.html", context=context)


class BookListView(generic.ListView):
    model = Book
    queryset = Book.objects.filter(title__icontains="Doraemon")[:5]
    context_object_name = "book_list"
    template_name = "catalog/book_list.html"


class BookDetailView(generic.DetailView):
    model = Book


def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)

    return render(request, "catalog/book_detail.html", context={"book": book})
