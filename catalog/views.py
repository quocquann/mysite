from typing import Any
from django.shortcuts import render
from catalog.models import Book, BookInstance, Genre, Author
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.


def index(request):
    """View function for home page of site"""

    # Generate counts of some of the main object

    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    num_instances_available = BookInstance.objects.filter(status="a").count()

    num_authors = Author.objects.count()

    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "num_visits": num_visits,
    }

    return render(request, "index.html", context=context)


class BookListView(generic.ListView):
    model = Book
    queryset = Book.objects.filter(title__icontains="Doraemon")[:5]
    context_object_name = "book_list"
    template_name = "catalog/book_list.html"


class BookDetailView(generic.DetailView):
    model = Book


class LoanBookByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance

    queryset = BookInstance.objects.filter(status="o")
    context_object_name = "bookinstance_list"
    template_name = "catalog/bookinstance_list_borrowed_user.html"


def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)

    return render(request, "catalog/book_detail.html", context={"book": book})
