from django.db import models
from django.urls import reverse
import uuid
from django.utils.translation import gettext_lazy as _
from .utils.constants import LOAN_STATUS


# Create your models here.


class Genre(models.Model):
    """Model representing a book genre."""

    name = models.CharField(max_length=200, help_text=_("Enter your book genre"))

    def __str__(self):
        """Return name of Genre objects"""
        return self.name


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""

    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)
    """on_delete option:
    - CASCADE
    - PROTECT
    - RESTRICT
    - SET_DEFAULT
    - SET
    - DO_NOTHING
    """

    summary = models.TextField(max_length=1000, help_text=_("Enter your summary"))
    isbn = models.CharField(
        "ISBN",
        max_length=13,
        unique=True,
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>',
    )

    genre = models.ManyToManyField(Genre, help_text=_("Select a genre for this book"))

    def __str__(self):
        """Return title of book objects"""
        return self.title

    def get_absolute_url(self):
        """Returns a URL for displaying individual model records on the website"""
        return reverse("book-detail", args=[str(self.id)])

    def display_genre(self):
        return ", ".join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = "Genre"


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID for this particular bookacross whole library",
    )
    book = models.ForeignKey("Book", on_delete=models.RESTRICT)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default="m",
        help_text="Book availability",
    )

    class Meta:
        """Declare model-level metadata for Model"""

        # Books are ordered by 'due_back' value by default
        ordering = ["due_back"]

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.id} ({self.book.title})"


class Author(models.Model):
    """Model representing an author."""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField("Died", null=True, blank=True)

    class Meta:
        # Author are ordered by 'last_name' and 'fist_name' by default
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        """Returns a URL for displaying individual model records on the website"""
        return reverse("author-detail", args=[str(self.id)])

    def __str__(self):
        """Return string representing last name and first name of Author objects"""
        return f"{self.last_name}, {self.first_name}"
