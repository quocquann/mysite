from rest_framework.serializers import ModelSerializer, Serializer, ValidationError
from rest_framework import serializers
from catalog.models import Book, BookInstance
from django.utils.translation import gettext_lazy as _
import datetime


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "author", "summary", "isbn", "genre"]


class RenewBookSerializer(Serializer):
    renewal_date = serializers.DateField()

    def validate_renewal_date(self, value):
        # Check if a date is not in the past.
        if value < datetime.date.today():
            raise ValidationError(_("Invalid date - renewal in past"))
        # Check if a date is in the allowed range (+4 weeks from today).
        if value > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_("Invalid date - renewal more than 4 weeks ahead"))
        # Remember to always return the cleaned data.
        return value


class BookInstanceSerializer(ModelSerializer):
    class Meta:
        model = BookInstance
        fields = ["id", "book", "imprint", "due_back", "status", "borrower"]
