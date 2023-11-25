from rest_framework.serializers import ModelSerializer
from catalog.models import Book


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "author", "summary", "isbn", "genre"]
