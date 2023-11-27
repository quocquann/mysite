from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from catalog.models import Book
from .serializers import BookSerializer


class BookList(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
