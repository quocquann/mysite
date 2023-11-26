from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from catalog.models import Book, BookInstance
from .serializers import BookSerializer, RenewBookSerializer, BookInstanceSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import CanMarkAsReturned


class BookList(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class BookDetail(APIView):
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()


class BookInstanceDetail(APIView):
    permission_classes = [IsAuthenticated, CanMarkAsReturned]

    def patch(self, request, pk):
        book = get_object_or_404(BookInstance, pk=pk)
        serializer = RenewBookSerializer(data=request.data)
        if serializer.is_valid():
            book.due_back = serializer.data["renewal_date"]
            book.save()
            serializer = BookInstanceSerializer(book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
