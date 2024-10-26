from .models import MyBook
from django.http import JsonResponse

def all_books_from_collection(request):
    if request.method == "GET":
        books = MyBook.objects.all().values()
        response = JsonResponse(list(books), safe=False)
        return response
    
def all_books_from_collection_id(request, book_id):
    if request.method == "GET":
        try:
            book = MyBook.objects.get(id=book_id)
            book_data = {
                "id": book.id,
                "book_title": book.book_title,
                "author": book.author,  
                "book_description": book.book_description
            }
            response = JsonResponse(book_data, safe=False)
            return response
        except MyBook.DoesNotExist:
            return JsonResponse({"message":"Book does not exist"}, safe=False, status=404)
    
