from .models import MyBook
from django.http import JsonResponse
import json
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict


#   data = {
#     "book_title": "Pat a Mat dokážou cokoliv ",
#     "author": "MK",
#     "book_description": "Dětská kniha",
#     "rating": null,
#     "created_by": "panenka",
#     "image": "https://rezised-images.knhbt.cz/880x880/31042988.webp",
#     "category": "other"}
@csrf_exempt  
def all_books_from_collection(request):
    if request.method == "GET":
        books = MyBook.objects.all().order_by('-date').values('book_title','author', 'book_description', 'image', 'category', 'rating', 'created_by__username')
        books_with_renamed_field = [
            {
                **book,
                'created_by': book.pop('created_by__username')
            }
                for book in books
            ]
        response = JsonResponse(books_with_renamed_field, safe=False)
        return response    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = User.objects.get(username=data["created_by"])
            book = MyBook (book_title = data["book_title"], author= data["author"], book_description=data["book_description"], image=data["image"], category=data["category"], rating=data["rating"],created_by=user)
            book.save()
            book_data = {
                    "id": book.id,
                    "book_title": book.book_title,
                    "author": book.author,  
                    "book_description": book.book_description, 
                    "rating": book.rating, 
                    "created_by": book.created_by.username, 
                    "image":book.image, 
                    "category":book.category
                }
            response = JsonResponse(book_data, safe=False)
            return response
        except KeyError:
            return JsonResponse({"message": "Missing required data"}, safe=False, status=400)
        except User.DoesNotExist:
            return JsonResponse({"message": "User not found"}, safe=False, status=400)
    return JsonResponse ({"message":"Invalid request method"}, safe=False, status=405)

@csrf_exempt   
def all_books_from_collection_id(request, book_id):
    if request.method == "GET":
        try:
            book = MyBook.objects.get(id=book_id)
            book_data = {
                "id": book.id,
                "book_title": book.book_title,
                "author": book.author,  
                "book_description": book.book_description, 
                "rating": book.rating, 
                "created_by": book.created_by.username, 
                "image":book.image, 
                "category":book.category

            }
            response = JsonResponse(book_data, safe=False)
            return response
        except MyBook.DoesNotExist:
            return JsonResponse({"message":"Book does not exist"}, safe=False, status=404)
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            if not "book_title" in data or not "author" in data or not "book_description" in data or not "image" in data or not "category" in data or not "rating" and "created_by" in data:
                return JsonResponse({"message": "Missing required data"}, safe=False, status=400)
            book = MyBook.objects.get(id=book_id)
            user = User.objects.get(username=data["created_by"])
            book.book_title = data["book_title"]
            book.author = data["author"]
            book.book_description = data["book_description"]
            book.rating = data["rating"]
            book.image = data["image"]
            book.category = data["category"]
            book.created_by = user
            book.save()
            book_data = {
                    "id": book.id,
                    "book_title": book.book_title,
                    "author": book.author,  
                    "book_description": book.book_description, 
                    "rating": book.rating, 
                    "created_by": book.created_by.username, 
                    "image":book.image, 
                    "category":book.category
                }
            response = JsonResponse(book_data, safe=False)
            return response
        except MyBook.DoesNotExist:
            return JsonResponse({"message":"Book does not exist"}, safe=False, status=404)
        except User.DoesNotExist:
            return JsonResponse({"message":"User does not exist"}, safe=False, status=400)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"message":"Invalid body"}, safe=False, status=400)
        
        
    if request.method == "DELETE":
        try:
            book = MyBook.objects.get(id=book_id)
            book.delete()
            return JsonResponse({"message": "Book deleted successfully"}, status=200, safe=False)
        except MyBook.DoesNotExist:
            return JsonResponse({"message":"Book does not exist"}, safe=False, status=404)
    return JsonResponse ({"message":"Invalid request method"}, safe=False, status=405)
        
    