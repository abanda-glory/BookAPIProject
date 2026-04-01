from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.conf import settings
from bson import ObjectId
from bson.errors import InvalidId

# Get books collection from MongoDB
books_col = settings.MONGO_DB['books']


def serialize_book(book):
    """Convert MongoDB document to JSON serializable dict"""
    book['id'] = str(book['_id'])
    del book['_id']
    return book


# Public - anyone can view books
@api_view(['GET'])
@permission_classes([AllowAny])
def book_list_public(request):
    books = list(books_col.find())
    return Response([serialize_book(b) for b in books])


# Protected - JWT token required
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def book_list(request):

    if request.method == 'GET':
        query = request.GET.get('search', '')
        if query:
            books = list(books_col.find({
                '$or': [
                    {'title': {'$regex': query, '$options': 'i'}},
                    {'author': {'$regex': query, '$options': 'i'}}
                ]
            }))
        else:
            books = list(books_col.find())
        return Response([serialize_book(b) for b in books])

    elif request.method == 'POST':
        data = request.data
        book = {
            'title': data.get('title', ''),
            'author': data.get('author', ''),
            'description': data.get('description', ''),
            'genre': data.get('genre', ''),
            'published_year': data.get('published_year', None),
            'isbn': data.get('isbn', ''),
        }
        result = books_col.insert_one(book)
        book['id'] = str(result.inserted_id)
        del book['_id']
        return Response(book, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def book_detail(request, pk):
    try:
        obj_id = ObjectId(pk)
    except InvalidId:
        return Response(
            {'error': 'Invalid book ID'},
            status=status.HTTP_400_BAD_REQUEST
        )

    book = books_col.find_one({'_id': obj_id})
    if not book:
        return Response(
            {'error': 'Book not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        return Response(serialize_book(book))

    elif request.method == 'PUT':
        data = request.data
        updated = {
            'title': data.get('title', book.get('title')),
            'author': data.get('author', book.get('author')),
            'description': data.get('description', book.get('description')),
            'genre': data.get('genre', book.get('genre')),
            'published_year': data.get('published_year', book.get('published_year')),
            'isbn': data.get('isbn', book.get('isbn')),
        }
        books_col.update_one({'_id': obj_id}, {'$set': updated})
        updated['id'] = pk
        return Response(updated)

    elif request.method == 'DELETE':
        books_col.delete_one({'_id': obj_id})
        return Response(
            {'message': 'Book deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )