from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import User, UploadedBook
import requests
import json

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
        

def best_book():
    cards = []
    response = requests.get(url= 'https://api.nytimes.com/svc/books/v3/lists/full-overview.json', params = {'api-key':os.getenv("API_KEY")})
    data = response.json()
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


def more_about_book(category, number):
    response = requests.get(url= f'https://api.nytimes.com/svc/books/v3/lists/current/{category}.json', params = {'api-key':os.getenv("API_KEY")})
    data = response.json()
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
    tops5=[]
    for book in books[:5]:
        author = book['author']
        book_image = book['book_image']
        title = book['title']   
        top5=Book_top5(author, book_image, title)
        tops5.append(top5)
    return card, tops5, 


def more_info_a_book(request,category, number):
    if request.method == "GET":
        book, tops5 = more_about_book(category, number)
        return render(request, "more_info_a_book.html", {
            'book':book,
            'tops5': tops5
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
    
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        # uploaded_file.name = nazev PDF, ktere si vyberu takto: uploaded_file.name
        upload_file = UploadedBook (file_name=uploaded_file.name, author=request.user, file=uploaded_file)
        upload_file.save()
        return render(request, 'upload_file.html', {'file_name': uploaded_file.name})
    uploaded_books = UploadedBook.objects.filter(author=request.user).order_by('-date')
    return render(request, 'upload_file.html', {'uploaded_books': uploaded_books})
    
def best_sellers(request):
    cards = best_book()
    if len(cards) > 0:
        return render (request, "best_sellers.html", {
        "books":cards
        })
    else:
        return render(request, "no_data.html")
    
