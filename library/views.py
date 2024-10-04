from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import User, UploadedBook, MyBook
from spire.pdf import *
from spire.pdf.common import *
import requests
import json
from io import BytesIO
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator



# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import os


class Book_card:
    def __init__(self, category, author, book_image, description, title):
        self.category = category
        self.author = author
        self.book_image = book_image
        self.description = description
        self.title = title

class Book_card_info:
    def __init__(self, author, book_image, description, title, publisher, primary_isbn10, primary_isbn13, buy_links, category):
        self.author = author
        self.book_image = book_image
        self.description = description
        self.title = title
        self.publisher= publisher
        self.primary_isbn10 = primary_isbn10
        self.primary_isbn13 = primary_isbn13
        self.buy_links = buy_links
        self.category = category

class Book_top5:
    def __init__(self, author, book_image, title):
        self.author = author
        self.book_image = book_image
        self.title = title

def best_book(data):
    cards = []
    if 'results' in data:
        results = data ['results']
        lists = results['lists']
        for slovnik in lists:
            category = slovnik['list_name']
            books = slovnik['books']
            book_1 = books[0]
            author = book_1['author']
            book_image = book_1['book_image']
            description = book_1['description']
            title = book_1['title']
            card = Book_card(category, author, book_image, description, title) 
            cards.append(card)
    return cards


def more_about_book(data, number):
    # if 'results' in data:
    results = data ['results']
    category= results['list_name']
    books = results['books']
    book_1 = books[int(number)-1]
    author = book_1['author']
    book_image = book_1['book_image']
    description = book_1['description']
    title = book_1['title']
    publisher = book_1['publisher']
    primary_isbn10=book_1['primary_isbn10']
    primary_isbn13 = book_1['primary_isbn13']
    buy_links = book_1['buy_links']
    card = Book_card_info(author, book_image, description, title, publisher, primary_isbn10,primary_isbn13, buy_links, category)
    return card 

def top_5 (data):
    results = data ['results']
    books = results['books']
    tops5=[]
    for book in books[:5]:
        author = book['author']
        book_image = book['book_image']
        title = book['title']   
        top5=Book_top5(author, book_image, title)
        tops5.append(top5)
    return tops5
        


def more_info_a_book(request,category, number):
    if request.method == "GET":
        response = requests.get(url= f'https://api.nytimes.com/svc/books/v3/lists/current/{category}.json', params = {'api-key':os.getenv("API_KEY")})
        data = response.json()
        if 'results' in data:
            book  = more_about_book(data, number)
            tops5 = top_5(data)
            return render(request, "more_info_a_book.html", {
                'book':book,
                'tops5': tops5
            })
        else:
            return render(request, "no_data_book.html", {
                'category':category,
                'number': number
            })




def index(request):
    return render (request, "index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")

def best_sellers(request):
    response = requests.get(url= 'https://api.nytimes.com/svc/books/v3/lists/full-overview.json', params = {'api-key':os.getenv("API_KEY")})
    data = response.json()
    cards = best_book(data)
    if len(cards) > 0:
        return render (request, "best_sellers.html", {
        "books":cards
        })
    else:
        return render(request, "no_data.html")

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        if uploaded_file.content_type != 'application/pdf':
            uploaded_books = UploadedBook.objects.filter(author=request.user).order_by('-date')
            return render(request, 'upload_file.html', {'error': 'Only PDF files are allowed, try again!', 'uploaded_books': uploaded_books})
        # uploaded_file.name = nazev PDF, ktere si vyberu takto: uploaded_file.name
        upload_file = UploadedBook (file_name=uploaded_file.name, author=request.user, file=uploaded_file)
        upload_file.save()
        title, author_of_book = get_pdf_info(upload_file.file.path)
        upload_file.title=title
        upload_file.author_of_book=author_of_book
        upload_file.save()
        return HttpResponseRedirect(reverse("upload_file"))
    uploaded_books = UploadedBook.objects.filter(author=request.user).order_by('-date')
    return render(request, 'upload_file.html', {'uploaded_books': uploaded_books})

def delete_upload_file(request):
    if request.method == "POST":
        delete_upload_file = request.POST["delete_upload_file"]
        if not delete_upload_file:
            messages.error(request, "Book ID is missing.")
            return  HttpResponseRedirect(reverse('upload_file'))
        try:
            file = UploadedBook.objects.get(id=delete_upload_file, author=request.user)
            file.delete()
            messages.success(request, "Book deleted successfully!")
        except UploadedBook.DoesNotExist:
            messages.error(request, "Book not found or you do not have permission to delete this book.")
        return HttpResponseRedirect(reverse('upload_file'))

def get_pdf_info(path):
    doc = PdfDocument()
    doc.LoadFromFile(path)
    information = doc.DocumentInformation
    title = information.Title
    author_of_book = information.Author
    return title, author_of_book
    
def collection(request):
    if request.method == "GET":
        search_term = request.GET.get("search", '').strip()
        books = MyBook.objects.filter(
            Q(created_by=request.user) & (Q(book_title__icontains=search_term) | Q(author__icontains=search_term))
        ).order_by('-date')
        paginator = Paginator(books, 8) 
        page_number = request.GET.get("page", 1) 
        page_obj = paginator.get_page(page_number)
        list_stranek = [i for i in range(1, paginator.num_pages+1)]  
        return render(request, "collection.html", {"books": page_obj, "pages":list_stranek, "search_term":search_term})                                                             
    else: 
        book_title = request.POST["book_title"]
        author = request.POST["author"]
        book_description = request.POST ["book_description"]
        image = request.POST['image']
        category = request.POST['category']
        all_inf_my = MyBook (book_title=book_title, author=author, book_description=book_description, image=image, category=category, created_by=request.user)
        all_inf_my.save()
        return HttpResponseRedirect (reverse("collection"))
    
def delete(request):
    if request.method == "POST":
        delete_book_id = request.POST["delete_book_id"]
        if not delete_book_id:
            messages.error(request, "Book ID is missing.")
            return  HttpResponseRedirect(reverse('collection'))
        try:
            book = MyBook.objects.get(id=delete_book_id, created_by=request.user)
            book.delete()
            messages.success(request, "Book deleted successfully!")
        except MyBook.DoesNotExist:
            messages.error(request, "Book not found or you do not have permission to delete this book.")
        return HttpResponseRedirect(reverse('collection'))
        
def collection_edit(request, book_id):
    if request.method == "GET":
        book = MyBook.objects.get(id=book_id)
        return render(request, "edit_collection.html", {"book_title": book.book_title, "author":book.author, "book_description": book.book_description, 'category':book.category, "book_id":book_id})

def add_collection_form(request):
    if request.method == "GET":
        return render(request, "add_collection_form_book.html")

def collection_edit_upload(request):
    if request.method == "POST":
        book_id = request.POST["edit_book_id"]
        book_title = request.POST["book_title"]
        author = request.POST["author"]
        book_description = request.POST ["book_description"]
        category = request.POST ["category"]
        book = MyBook.objects.get(id=book_id)
        book.book_title = book_title
        book.author = author
        book.book_description = book_description
        book.category =category
        book.save()
        return render(request, "edit_collection_1.html", {
                'book':book
            })
    book_id = request.GET["book_id"]
    book = MyBook.objects.get(id=book_id)
    return render(request, "edit_collection_1.html", {
        'book': book  
    })
    







    
