from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import User
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


def best_book():
    cards = []
    response = requests.get(url= 'https://api.nytimes.com/svc/books/v3/lists/full-overview.json', params = {'api-key':os.getenv("API_KEY")})
    data = response.json()
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


def index(request):
    return render (request, "index.html", {
        "books":best_book()
    })

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