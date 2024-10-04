from django.test import TestCase
from library.views import best_book, more_about_book, top_5

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from .models import User, UploadedBook, MyBook

class Book_test(TestCase):
    def test_best_book_I(self):
        data = {}
        cards = best_book(data)
        self.assertEqual(cards, [])
    
    def test_best_book_II(self):
        data = {
            "results": {
                "lists": [
                {
                    "list_name": "Romantic",
                    "books": [
                    {
                        "author": "Mona Kasten",
                        "book_image": "krket",
                        "description": "Romantic story",
                        "title": "Never say never"
                    }
                    ]
                }
                ]
            }
            }
        cards = best_book(data)
        self.assertEqual(cards[0].category, "Romantic")
        self.assertEqual(cards[0].author, "Mona Kasten")
        self.assertEqual(cards[0].book_image, "krket")
        self.assertEqual(cards[0].description, "Romantic story")
        self.assertEqual(cards[0].title, "Never say never")
        self.assertEqual(len(cards), 1)


    def test_more_about_book_I(self):
        data = {
             "results": {
                  "list_name": "Romantic",
                  "books":[
                       {
                            "author":"Mona Kasten",
                            "book_image": "pat a mat",
                            "description": "romantic book",
                            "title": "Never say never II", 
                            "publisher": "Penguin", 
                            "primary_isbn10": "0143127748", 
                            "primary_isbn13": "9780143127741", 
                            "buy_links": [
                                 {
                                    "name": "Amazon",
                                    "url": "http://www.amazon.com/The-Body-Keeps-Score-Healing/dp/0670785938?tag=thenewyorktim-20"
                                 }, 
                                 {
                                    "name": "Apple Books",
                                    "url": "https://goto.applebooks.apple/9780143127741?at=10lIEQ"
                                 }, 
                                 {
                                    "name": "Barnes and Noble",
                                    "url": "x"
                                 }, 
                                 {
                                    "name": "Books-A-Million",
                                    "url": "z"
                                },
                            ]
                       }
                  ]

                  
             }
             
        }
        card = more_about_book(data, 1)
        self.assertEqual(card.author, "Mona Kasten")
        self.assertEqual(card.book_image, "pat a mat")
        self.assertEqual(card.description, "romantic book")
        self.assertEqual(card.title, "Never say never II")
        self.assertEqual(card.publisher, "Penguin")
        self.assertEqual(card.primary_isbn10, "0143127748")
        self.assertEqual(card.primary_isbn13, "9780143127741")

        self.assertEqual(card.buy_links[0]["name"], "Amazon")
        self.assertEqual(card.buy_links[0]["url"], "http://www.amazon.com/The-Body-Keeps-Score-Healing/dp/0670785938?tag=thenewyorktim-20")
        self.assertEqual(card.buy_links[1]["name"], "Apple Books")
        self.assertEqual(card.buy_links[1]["url"], "https://goto.applebooks.apple/9780143127741?at=10lIEQ")
        self.assertEqual(card.buy_links[2]["name"], "Barnes and Noble")
        self.assertEqual(card.buy_links[2]["url"], "x")
        self.assertEqual(card.buy_links[3]["name"], "Books-A-Million")
        self.assertEqual(card.buy_links[3]["url"], "z")


    def test_top_5(self):
        data = {
             "results": {
                 "books":[
                       {
                            "author":"Mona Kasten",
                            "book_image": "pat a mat",
                            "description": "romantic book",
                            "title": "Never say never II",  
                       }, 
                        {
                            "author":"x",
                            "book_image": "xx",
                            "description": "xxx",
                            "title": "xxxx",  
                       }, 
                        {
                            "author":"z",
                            "book_image": "zz",
                            "description": "zzz",
                            "title": "zzzz",  
                       },
                        {
                            "author":"y",
                            "book_image": "yy",
                            "description": "yyy",
                            "title": "yyyy",  
                       },
                       {
                            "author":"m",
                            "book_image": "mm",
                            "description": "mmm",
                            "title": "mmmm",  
                       }, 
                       {
                            "author":"k",
                            "book_image": "kk",
                            "description": "kkk",
                            "title": "kkkk",  
                       },

                 ]
             }
        }
        top5 = top_5(data)
        self.assertEqual(top5[0].author, "Mona Kasten")
        self.assertEqual(top5[0].book_image, "pat a mat")
        self.assertEqual(top5[0].title, "Never say never II")

        self.assertEqual(top5[1].author, "x")
        self.assertEqual(top5[1].book_image, "xx")
        self.assertEqual(top5[1].title, "xxxx")

        self.assertEqual(top5[2].author, "z")
        self.assertEqual(top5[2].book_image, "zz")
        self.assertEqual(top5[2].title, "zzzz")

        self.assertEqual(top5[3].author, "y")
        self.assertEqual(top5[3].book_image, "yy")
        self.assertEqual(top5[3].title, "yyyy")

        self.assertEqual(top5[4].author, "m")
        self.assertEqual(top5[4].book_image, "mm")
        self.assertEqual(top5[4].title, "mmmm")
        self.assertEqual(len(top5), 5)

class MyUserIn(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
    
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp (self):
        user = User.objects.create_superuser(username='hroch', password='big_hippo', email='hippo@test.com', is_active=True)
        user.save()

    def login(self):
        self.selenium.get(f"{self.live_server_url}/login")
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("hroch")
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("big_hippo")
        self.selenium.find_element(By.XPATH, '//input[@value="Login"]').click()
    
    def test_login(self):
        self.login()
        title = self.selenium.find_element(By.CLASS_NAME, "title_bestsellers")
        self.assertEqual(title.text, "Best sellers")
    
    def test_register(self):
        self.selenium.get(f"{self.live_server_url}/register")
        h2 = self.selenium.find_element(By.TAG_NAME, "h2")
        self.assertEqual(h2.text, "Register")
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("balon")
        email_input = self.selenium.find_element(By.NAME, "email")
        email_input.send_keys("balon@bal.cz")
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("big")
        password_confirmation_input = self.selenium.find_element(By.NAME, "confirmation")
        password_confirmation_input.send_keys("big")
        self.selenium.find_element(By.XPATH, '//input[@value="Register"]').click()
        title = self.selenium.find_element(By.CLASS_NAME, "title_bestsellers")
        self.assertEqual(title.text, "Best sellers")
        
