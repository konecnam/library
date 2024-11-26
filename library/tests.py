from django.test import TestCase
from library.views import best_book, more_about_book, top_5
from django.urls import reverse

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from .models import User, UploadedBook, MyBook
from selenium.webdriver.support.ui import Select
import time, unittest
from django.test import Client
import responses
from .full_overview import FULL_OVERVIEW
from .category import COMBINED_PRINT_AND_EBOOK_FICTION


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

    def test_add_book(self):
        self.login()
        link = self.selenium.find_element(By.XPATH,'/html/body/div/div/header/div[2]/nav/a[2]')
        link.click()
        add_book = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[1]/button/span')
        add_book.click()

        book_title = self.selenium.find_element(By.NAME, "book_title")
        book_title.send_keys("Zacit znovu")
        author = self.selenium.find_element(By.NAME, "author")
        author.send_keys("Mona Kasten")
        book_description = self.selenium.find_element(By.NAME, "book_description")
        book_description.send_keys("Romantic books")
        image = self.selenium.find_element(By.NAME, "image")
        image.send_keys("https://cdn.palmknihy.cz/prod-media-assets/01G6JVHKM658H6P5Z3ZN8HWC9W/0302400-20.jpg?v=ed3de541")

        category_dropdown = Select(self.selenium.find_element(By.NAME, "category"))
        category_dropdown.select_by_visible_text("Romantic") 
        save = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/form[1]/input[2]')
        save.click()
        title = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/div[1]/div[2]/div/h5[1]')
        self.assertEqual(title.text, "Zacit znovu")
        author = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/div[1]/div[2]/div/h5[2]')
        self.assertEqual(author.text, "Mona Kasten")
        book_description = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/div[1]/div[2]/div/p[1]')
        self.assertEqual(book_description.text, "Book description: Romantic books")
        image = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/div[1]/div[1]/div')
        background_image = image.value_of_css_property('background')
        background_image_url = background_image.split('"')[1]
        self.assertEqual(background_image_url, "https://cdn.palmknihy.cz/prod-media-assets/01G6JVHKM658H6P5Z3ZN8HWC9W/0302400-20.jpg?v=ed3de541")
        
        self.assertEqual(book_description.text, "Book description: Romantic books")
        category = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/div[1]/div[2]/div/p[2]')
        self.assertEqual(category.text, "Category: Romantic")

    def test_add_book_none(self):
        self.login()
        link = self.selenium.find_element(By.XPATH,'/html/body/div/div/header/div[2]/nav/a[2]')
        link.click()
        add_book = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[1]/button/span')
        add_book.click()
        category_dropdown = Select(self.selenium.find_element(By.NAME, "category"))
        category_dropdown.select_by_visible_text("Romantic") 
        save = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/form[1]/input[2]')
        save.click()
        text = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[1]/h5')
        self.assertEqual(text.text, "Not all fields are filled in!")


    def test_add_book_none_image(self):
        self.login()
        link = self.selenium.find_element(By.XPATH,'/html/body/div/div/header/div[2]/nav/a[2]')
        link.click()
        add_book = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[1]/button/span')
        add_book.click()
        book_title = self.selenium.find_element(By.NAME, "book_title")
        book_title.send_keys("Stále znovu")
        author = self.selenium.find_element(By.NAME, "author")
        author.send_keys("Mona Kasten")
        book_description = self.selenium.find_element(By.NAME, "book_description")
        book_description.send_keys("Romantic books")
        save = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/form[1]/input[2]')
        save.click()
        text = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[1]/h5')
        self.assertEqual(text.text, "Not all fields are filled in!")

    def test_edit(self):
        user = User.objects.get(username='hroch')
        all_inf_my = MyBook (book_title='Sexy pilot', author='XXX', book_description='eroticka kniha', image='xxx', category='Romantic', created_by=user)
        all_inf_my.save()
        self.login()
        link = self.selenium.find_element(By.XPATH,'/html/body/div/div/header/div[2]/nav/a[2]')
        link.click()
        edit = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/div[1]/div[2]/div/div/button')
        edit.click()

        title = self.selenium.find_element(By.XPATH, '//html/body/div/div/main/div/div[2]/div[1]/div[2]/form[1]/div[1]/input')
        title.clear()
        title.send_keys("Sexy profesor")
        author = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/div[1]/div[2]/form[1]/div[2]/input')
        author.clear()
        author.send_keys("ZZZ ")
        category_dropdown = Select(self.selenium.find_element(By.NAME, "category"))
        category_dropdown.select_by_visible_text("Other")
        submit = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div/div[1]/div[2]/form[1]/button[1]')
        submit.click()

        title = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div/div[1]/div[2]/div/h5[1]')
        self.assertEqual(title.text, "Sexy profesor")
        author = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div/div[1]/div[2]/div/h5[2]')
        self.assertEqual(author.text, "ZZZ")
        book_description = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div/div[1]/div[2]/div/p[1]')
        self.assertEqual(book_description.text, "Book description: eroticka kniha")
        image = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/div[1]/div[1]/div')
        background_image = image.value_of_css_property('background')
        background_image_url = background_image.split('"')[1]
        self.assertEqual(background_image_url, "xxx")
        category = self.selenium.find_element(By.XPATH, '//html/body/div/div/main/div/div/div[1]/div[2]/div/p[2]')
        self.assertEqual(category.text, "Category: Other")

    def test_edit_cancel(self):
        user = User.objects.get(username='hroch')
        all_inf_my = MyBook (book_title='Sexy pilot', author='XXX', book_description='eroticka kniha', image='xxx', category='Romantic', created_by=user)
        all_inf_my.save()
        self.login()
        link = self.selenium.find_element(By.XPATH,'/html/body/div/div/header/div[2]/nav/a[2]')
        link.click()
        edit = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/div[1]/div[2]/div/div/button')
        edit.click()

        title = self.selenium.find_element(By.XPATH, '//html/body/div/div/main/div/div[2]/div[1]/div[2]/form[1]/div[1]/input')
        title.clear()
        title.send_keys("Sexy profesor")
        author = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/div[1]/div[2]/form[1]/div[2]/input')
        author.clear()
        author.send_keys("ZZZ ")
        book_description = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/div[1]/div[2]/form[1]/div[3]/input')
        category_dropdown = Select(self.selenium.find_element(By.NAME, "category"))
        category_dropdown.select_by_visible_text("Other")
        cancel = self.selenium.find_element(By.XPATH, '//html/body/div/div/main/div/div[2]/div[1]/div[2]/form[1]/button[2]')
        cancel.click()
        title = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div/div[1]/div[2]/div/h5[1]')
        self.assertEqual(title.text, "Sexy pilot")
        author = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div/div[1]/div[2]/div/h5[2]')
        self.assertEqual(author.text, "XXX")
        book_description = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div/div[1]/div[2]/div/p[1]')
        self.assertEqual(book_description.text, "Book description: eroticka kniha")
        category = self.selenium.find_element(By.XPATH, '//html/body/div/div/main/div/div/div[1]/div[2]/div/p[2]')
        self.assertEqual(category.text, "Category: Romantic")
    
    def test_delete(self):
        user = User.objects.get(username='hroch')
        all_inf_my = MyBook (book_title='YYY', author='XXX', book_description='ZZZ', image='xxx', category='Romantic', created_by=user)
        all_inf_my.save()
        self.login()
        link = self.selenium.find_element(By.XPATH,'/html/body/div/div/header/div[2]/nav/a[2]')
        link.click()
        title = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/div[1]/div[2]/div/h5[1]')
        self.assertEqual(title.text, "YYY")
        author = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/div[1]/div[2]/div/h5[2]')
        self.assertEqual(author.text, "XXX")
        book_description = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/div[1]/div[2]/div/p[1]')
        self.assertEqual(book_description.text, "Book description: ZZZ")
        delete = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/div[1]/div[2]/div/div/form/button/i')
        delete.click()
        with self.assertRaises(MyBook.DoesNotExist):
            MyBook.objects.get(book_title='YYY', author='XXX', book_description='ZZZ')
    
    def test_stars(self):
        user = User.objects.get(username='hroch')
        all_inf_my = MyBook (book_title='YYY', author='XXX', book_description='ZZZ', image='xxx', category='Romantic', created_by=user)
        all_inf_my.save()
        self.login()
        link = self.selenium.find_element(By.XPATH,'/html/body/div/div/header/div[2]/nav/a[2]')
        link.click()
        stars = self.selenium.find_element(By. XPATH, '/html/body/div/div/main/div/div[2]/div[1]/div[2]/form/label[3]/span[3]')
        stars.click()
        new_book = MyBook.objects.get(book_title='YYY', author='XXX', book_description='ZZZ')
        self.assertEqual(new_book.rating, 3)

    def test_page(self):
        user = User.objects.get(username='hroch')
        for i in range(1, 10):  
            MyBook(
                book_title=f'book_title {i}',
                author=f'author {i}',
                book_description=f'book_description {i}',
                image=f'image {i}',
                category='Romantic',
                created_by=user
                ).save()
            time.sleep(1)
        self.login()
        link = self.selenium.find_element(By.XPATH,'/html/body/div/div/header/div[2]/nav/a[2]')
        link.click()
        first = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/div[1]/div[2]/div/h5[1]')
        self.assertEqual(first.text, "book_title 9")
        two = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/div[8]/div[2]/div/h5[1]')
        self.assertEqual(two.text, "book_title 2")
        page_2 = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/nav/ul/li[2]/a')
        page_2.click()
        one = self.selenium.find_element(By.XPATH,'/html/body/div/div/main/div/div[2]/div[1]/div[2]/div/h5[1]')
        self.assertEqual(one.text, "book_title 1")
    
    def test_page_next(self):
        user = User.objects.get(username='hroch')
        for i in range(1, 22):  
            MyBook(
                book_title=f'book_title {i}',
                author=f'author {i}',
                book_description=f'book_description {i}',
                image=f'image {i}',
                category='Romantic',
                created_by=user
                ).save()
            time.sleep(0.1)
        self.login()
        link = self.selenium.find_element(By.XPATH,'/html/body/div/div/header/div[2]/nav/a[2]')
        link.click()
        page_finish = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/nav/ul/a')
        page_finish.click()
        one = self.selenium.find_element(By.XPATH,'/html/body/div/div/main/div/div[2]/div[8]/div[2]/div/h5[1]')
        self.assertEqual(one.text, "book_title 6")
        back = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/nav/ul/li[1]/a')
        back.click()
        book_14 = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/div[8]/div[2]/div/h5[1]')
        self.assertEqual(book_14.text, "book_title 14")
    
    def test_search(self):
        user = User.objects.get(username='hroch')
        first_book = MyBook (book_title='miluji tě', author='Mona Kasten', book_description='ZZZ', image='xxx', category='Romantic', created_by=user)
        first_book.save()
        second_book = MyBook (book_title='auto', author='Julie Caplinova', book_description='BBB', image='AAA', category='Romantic', created_by=user)
        second_book.save()
        self.login()
        link = self.selenium.find_element(By.XPATH,'/html/body/div/div/header/div[2]/nav/a[2]')
        link.click()
        search = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/form/div/div/input')
        search.send_keys('miluji')
        button_search = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/form/button')
        button_search.click()
        result = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/div/div[2]/div/h5[1]')
        self.assertEqual('miluji tě', result.text)

    def test_search_2(self):
        user = User.objects.get(username='hroch')
        first_book = MyBook (book_title='miluji tě', author='Mona Kasten', book_description='ZZZ', image='xxx', category='Romantic', created_by=user)
        first_book.save()
        second_book = MyBook (book_title='auto', author='Miluj Caplinova', book_description='BBB', image='AAA', category='Romantic', created_by=user)
        second_book.save()
        self.login()
        link = self.selenium.find_element(By.XPATH,'/html/body/div/div/header/div[2]/nav/a[2]')
        link.click()
        search = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/form/div/div/input')
        search.send_keys('milu')
        button_search = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/form/button')
        button_search.click()
        result_1 = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/div/div[2]/div/h5[1]')
        self.assertEqual('miluji tě', result_1.text)
        result_2 = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/div[2]/div[2]/div/h5[2]')
        self.assertEqual('Miluj Caplinova', result_2.text)

    def test_search_3(self):
        user = User.objects.get(username='hroch')
        first_book = MyBook (book_title='miluji tě', author='Mona Kasten', book_description='ZZZ', image='xxx', category='Romantic', created_by=user)
        first_book.save()
        second_book = MyBook (book_title='auto', author='Julie Caplinova', book_description='BBB', image='AAA', category='Romantic', created_by=user)
        second_book.save()
        self.login()
        link = self.selenium.find_element(By.XPATH,'/html/body/div/div/header/div[2]/nav/a[2]')
        link.click()
        search = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/form/div/div/input')
        search.send_keys('bla')
        button_search = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/form/button')
        button_search.click()
        result = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/h5')
        self.assertEqual('No books saved yet.', result.text)

class MyBestSellers(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
    
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    @responses.activate
    def test_best_seller(self):
        rsp1 = responses.Response(
        method="GET",
        url="https://api.nytimes.com/svc/books/v3/lists/full-overview.json", 
        json=FULL_OVERVIEW,
        status=200)
        responses.add(rsp1)
        self.selenium.get(self.live_server_url)
        title = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/h4')
        self.assertEqual("Best sellers", title.text)

        category_first = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div/div/div[1]/div[1]/span/span')
        self.assertEqual(category_first.text, "Combined Print and E-Book Fiction")
        more_info = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div/div/div[1]/div[2]/a')
        self.assertEqual(more_info.text, "MORE INFORMATION")
        book_description_first = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div/div/div[1]/div[3]')
        self.assertEqual(book_description_first.text, "HEXED, Emily McIntire\nThe sixth book in the Never After series. A forbidden love develops between the underboss to a mafia syndicate and his fiancée's cousin.")
        category_last = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div/div/div[18]/div[1]/span/span')
        self.assertEqual(category_last.text, "Young Adult Paperback Monthly")
        book_description_last=self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div/div/div[18]/div[3]')
        self.assertEqual (book_description_last.text, "IF HE HAD BEEN WITH ME, Laura Nowlin")

    @responses.activate
    def test_more(self):
        rsp1 = responses.Response(
        method="GET",
        url="https://api.nytimes.com/svc/books/v3/lists/full-overview.json", 
        json=FULL_OVERVIEW,
        status=200)
        responses.add(rsp1)

        rsp2 = responses.Response(
        method="GET",
        url="https://api.nytimes.com/svc/books/v3/lists/current/combined-print-and-e-book-fiction.json", 
        json= COMBINED_PRINT_AND_EBOOK_FICTION,
        status=200)
        responses.add(rsp2)
        self.selenium.get(self.live_server_url)

        more_info = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div/div/div[1]/div[2]/a')
        more_info.click()
        title = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[1]/div[2]/h3')
        self.assertEqual(title.text, "TO DIE FOR")
        author = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[1]/div[2]/h4')
        self.assertEqual(author.text, "Author: David Baldacci")
        book_description = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[1]/div[2]/p[1]')
        self.assertEqual(book_description.text, "The third book in the 6:20 Man series. Devine digs into the deaths of an orphan’s parents and uncovers a large conspiracy.")
        publish = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[1]/div[2]/p[2]')
        self.assertEqual(publish.text, "Publisher: Grand Central")
        ISBN = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[1]/div[2]/p[3]')
        self.assertEqual(ISBN.text, "ISBN 10: 1538757931\nISBN 13: 9781538757932")
        book_5 = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[3]/div[5]/a/div')
        book_5.click()
        author_5 = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[1]/div[2]/h3')
        self.assertEqual(author_5.text, "A COURT OF THORNS AND ROSES")

    @responses.activate
    def test_add_to_collection(self):
        user = User.objects.create_superuser(username='hroch', password='big_hippo', email='hippo@test.com', is_active=True)
        user.save()
        self.selenium.get(f"{self.live_server_url}/login")
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("hroch")
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("big_hippo")
        self.selenium.find_element(By.XPATH, '//input[@value="Login"]').click()

        rsp1 = responses.Response(
        method="GET",
        url="https://api.nytimes.com/svc/books/v3/lists/full-overview.json", 
        json=FULL_OVERVIEW,
        status=200)
        responses.add(rsp1)

        rsp2 = responses.Response(
        method="GET",
        url="https://api.nytimes.com/svc/books/v3/lists/current/combined-print-and-e-book-fiction.json", 
        json= COMBINED_PRINT_AND_EBOOK_FICTION,
        status=200)
        responses.add(rsp2)
        self.selenium.get(self.live_server_url)
        more_info = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div/div/div[1]/div[2]/a')
        more_info.click()
        add_to_collection = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[1]/div[2]/form/label/span')
        add_to_collection.click()
        title= self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[2]/div/div[2]/div/h5[1]')
        self.assertEqual(title.text, "TO DIE FOR")
        # kontrola zda je to v databazi
        book = MyBook.objects.get(book_title='TO DIE FOR')
        self.assertEqual(book.book_title, "TO DIE FOR")
        self.assertEqual(book.author, "David Baldacci")
        self.assertEqual(book.book_description, "The third book in the 6:20 Man series. Devine digs into the deaths of an orphan’s parents and uncovers a large conspiracy.")
        self.assertIsNone(book.rating)
        self.assertEqual(book.created_by.username, "hroch")
        self.assertEqual(book.image, "https://storage.googleapis.com/du-prd/books/images/9781538757901.jpg")
        self.assertEqual(book.category, "Other")

    @responses.activate
    def test_status_400(self):
        rsp1 = responses.Response(
        method="GET",
        url="https://api.nytimes.com/svc/books/v3/lists/full-overview.json", 
        json={},
        status=400)
        responses.add(rsp1) 
        self.selenium.get(self.live_server_url)
        no_data = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div/h3[1]')
        self.assertEqual(no_data.text, "Could not load bestsellers list from New York Times!")
    
    @responses.activate
    def test_status_400_more_info(self):
        rsp1 = responses.Response(
        method="GET",
        url="https://api.nytimes.com/svc/books/v3/lists/full-overview.json", 
        json=FULL_OVERVIEW,
        status=200)
        responses.add(rsp1)

        rsp2 = responses.Response(
        method="GET",
        url="https://api.nytimes.com/svc/books/v3/lists/current/combined-print-and-e-book-fiction.json", 
        json= {},
        status=400)
        responses.add(rsp2)
        self.selenium.get(self.live_server_url)
        more_info = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div/div/div[1]/div[2]/a')
        more_info.click()
        no_data = self.selenium.find_element(By.CLASS_NAME, 'title_no_data')
        self.assertEqual(no_data.text, "Could not load list from New York Times!")
    
    @responses.activate
    def test_status_400_more_info_again(self):
        rsp1 = responses.Response(
        method="GET",
        url="https://api.nytimes.com/svc/books/v3/lists/full-overview.json", 
        json=FULL_OVERVIEW,
        status=200)
        responses.add(rsp1)

        rsp2= responses.Response(
        method="GET",
        url="https://api.nytimes.com/svc/books/v3/lists/current/combined-print-and-e-book-fiction.json", 
        json= {},
        status=400)
        responses.add(rsp2)

        rsp3 = responses.Response(
        method="GET",
        url="https://api.nytimes.com/svc/books/v3/lists/current/combined-print-and-e-book-fiction.json", 
        json= COMBINED_PRINT_AND_EBOOK_FICTION,
        status=200)
        responses.add(rsp3)

        self.selenium.get(self.live_server_url)
        more_info = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div/div/div[1]/div[2]/a')
        more_info.click()
        no_data = self.selenium.find_element(By.CLASS_NAME, 'title_no_data')
        self.assertEqual(no_data.text, "Could not load list from New York Times!")
        again_here  = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/h3[2]/a')
        again_here.click()
        title = self.selenium.find_element(By.XPATH, '/html/body/div/div/main/div/div[1]/div[2]/h3')
        self.assertEqual(title.text, "TO DIE FOR")

        







        


    

class RestApiTest(unittest.TestCase):
    
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        # Vymažeme všechny záznamy z tabulek v databázi
        MyBook.objects.all().delete()
        User.objects.all().delete()

    def test_post(self):
        User.objects.create(username='panenka')
        response = self.client.post(reverse('all_books_from_collection'), data={
            "book_title": "Happy",
            "author": "DD",
            "book_description": "Dětská kniha",
            "rating": "2",
            "created_by": "panenka",
            "image": "https://rezised-images.knhbt.cz/880x880/31042988.webp",
            "category": "other"
        }, content_type="application/json")
        book_info = response.json()
        self.assertEqual(book_info["book_title"], "Happy")
        self.assertEqual(book_info["author"], "DD")
        self.assertEqual(book_info["book_description"], "Dětská kniha")
        self.assertEqual(book_info["rating"], "2")
        self.assertEqual(book_info["created_by"], "panenka")
        self.assertEqual(book_info["image"], "https://rezised-images.knhbt.cz/880x880/31042988.webp")
        self.assertEqual(book_info["category"], "other")
        self.assertNotEqual(book_info["id"], None)
        self.assertEqual(response.status_code, 200)
        #kontrola zda je to v databazi
        book = MyBook.objects.get(id=book_info["id"])
        self.assertEqual(book.book_title, "Happy")
        self.assertEqual(book.author, "DD")
        self.assertEqual(book.book_description, "Dětská kniha")
        self.assertEqual(book.rating, 2)
        self.assertEqual(book.created_by.username, "panenka")
        self.assertEqual(book.image, "https://rezised-images.knhbt.cz/880x880/31042988.webp")
        self.assertEqual(book.category, "other")

    def test_post_put(self):
        User.objects.create(username='panenka')
        response = self.client.put(reverse('all_books_from_collection'), data={
            "book_title": "Happy",
            "author": "DD",
            "book_description": "Dětská kniha",
            "rating": "2",
            "created_by": "panenka",
            "image": "https://rezised-images.knhbt.cz/880x880/31042988.webp",
            "category": "other"
        }, content_type="application/json")
        book_info = response.json()
        self.assertEqual(book_info["message"], "Invalid request method")
        self.assertEqual(response.status_code, 405)

    def test_missing_data(self):
        User.objects.create(username='panenka')
        response = self.client.post(reverse('all_books_from_collection'), data={
            "book_title": "Happy",
            "book_description": "Dětská kniha",
            "rating": "2",
            "created_by": "panenka",
            "image": "https://rezised-images.knhbt.cz/880x880/31042988.webp",
            "category": "other"
        }, content_type="application/json")
        book_info = response.json()
        self.assertEqual(book_info["message"], "Missing required data")
        self.assertEqual(response.status_code, 400)

    def test_user_not_found(self):
        response = self.client.post(reverse('all_books_from_collection'), data={
            "book_title": "Happy",
            "author": "DD",
            "book_description": "Dětská kniha",
            "rating": "2",
            "created_by": "slon",
            "image": "https://rezised-images.knhbt.cz/880x880/31042988.webp",
            "category": "other"
        }, content_type="application/json")
        book_info = response.json()
        self.assertEqual(book_info["message"], "User not found")
        self.assertEqual(response.status_code, 400)

    def test_get_all_book(self):
        user_1 = User.objects.create(username='panda')
        first_book_1= MyBook (book_title='CCC', author='Mona Kasten', book_description='ZZZ', image='xxx', category='Romantic', created_by=user_1, rating= "2",)
        first_book_1.save()

        user_2 = User.objects.create(username='hroch')
        second_book_0 = MyBook (book_title='auto', author='Julie Caplinova', book_description='BBB', image='AAA', category='Romantic', created_by=user_2, rating= "3",)
        second_book_0.save()

        response = self.client.get(reverse('all_books_from_collection'))
        self.assertEqual(response.status_code, 200)
        books = response.json()
        self.assertIsInstance(books, list)

        self.assertEqual (books[0]["book_title"], "auto")
        self.assertEqual (books[0]["author"], "Julie Caplinova")
        self.assertEqual (books[0]["book_description"], "BBB")
        self.assertEqual (books[0]["image"], "AAA")
        self.assertEqual (books[0]["category"], "Romantic")
        self.assertEqual (books[0]["created_by"], "hroch")
        self.assertEqual (books[0]["rating"], 3)

        self.assertEqual (books[1]["book_title"], "CCC")
        self.assertEqual (books[1]["author"], "Mona Kasten")
        self.assertEqual (books[1]["book_description"], "ZZZ")
        self.assertEqual (books[1]["image"], "xxx")
        self.assertEqual (books[1]["category"], "Romantic")
        self.assertEqual (books[1]["created_by"], "panda")
        self.assertEqual (books[1]["rating"], 2)
    
    def test_get_all_book(self):
        response = self.client.get(reverse('all_books_from_collection'))
        self.assertEqual(response.status_code, 200)
        books = response.json()
        len_books = len(books)
        self.assertEqual(len_books, 0)
    
    def test_get_book(self):
        self.client = Client()
        opice = User.objects.create(username='opice')
        book= MyBook (book_title='Bad', author='XXX', book_description='ZZZ', image='xxx', category='Fantasy', created_by=opice, rating= "4",)
        book.save()
        response = self.client.get(reverse('all_books_from_collection_id', args=[book.id]))
        book_info = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual (book_info["book_title"], "Bad")
        self.assertEqual (book_info["author"], "XXX")
        self.assertEqual (book_info["book_description"], "ZZZ")
        self.assertEqual (book_info["image"], "xxx")
        self.assertEqual (book_info["category"], "Fantasy")
        self.assertEqual (book_info["created_by"], "opice")
        self.assertEqual (book_info["rating"], 4)

    def test_get_no_book(self):
        book_id_notexist = 900
        response = self.client.get(reverse('all_books_from_collection_id', args=[book_id_notexist]))
        book_info = response.json()
        self.assertEqual(book_info["message"], "Book does not exist")
        self.assertEqual(response.status_code, 404)

    def test_delete_200(self):
        opice = User.objects.create(username='lenochod')
        book= MyBook (book_title='Sad', author='GGG', book_description='PPP', image='xxx', category='Fantasy', created_by=opice, rating= "4",)
        book.save()
        response = self.client.delete(reverse('all_books_from_collection_id', args=[book.id]))
        book_info = response.json()
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(MyBook.DoesNotExist):
            MyBook.objects.get(id = book.id)
        self.assertEqual(book_info["message"], "Book deleted successfully")
    
    def test_delete_404(self):
        book_id_notexist = 999
        response = self.client.delete(reverse('all_books_from_collection_id', args=[book_id_notexist]))
        book_info = response.json()
        self.assertEqual(book_info["message"], "Book does not exist")
        self.assertEqual(response.status_code, 404)

    def test_put(self):
        medved = User.objects.create(username='medved')
        book= MyBook (book_title='Lucky', author='LLL', book_description='UUU', image='CCC', category='Other', created_by=medved, rating= "5",)
        book.save()
        response = self.client.put(reverse('all_books_from_collection_id', args=[book.id]), 
            data =  {
            "book_title":"Funny", 
            "author":"FFF", 
            "book_description":"NNN",
            "image":"UUU", 
            "category":"Romantic", 
            "created_by":"medved", 
            "rating": "2"
            } , content_type="application/json"
        )
        #kontrola response vrati slovnik 
        book_info = response.json()
        self.assertEqual(book_info["book_title"], "Funny")
        self.assertEqual(book_info["author"], "FFF")
        self.assertEqual(book_info["book_description"], "NNN")
        self.assertEqual(book_info["rating"], "2")
        self.assertEqual(book_info["created_by"], "medved")
        self.assertEqual(book_info["image"], "UUU")
        self.assertEqual(book_info["category"], "Romantic")
        self.assertEqual(response.status_code, 200)
        #kontrola zda je to v databazi
        book = MyBook.objects.get(id=book_info["id"])
        self.assertEqual(book.book_title, "Funny")
        self.assertEqual(book.author, "FFF")
        self.assertEqual(book.book_description, "NNN")
        self.assertEqual(book.rating, 2)
        self.assertEqual(book.created_by.username, "medved")
        self.assertEqual(book.image, "UUU")
        self.assertEqual(book.category, "Romantic")
    
    def test_put_404_no_book(self):
        book_id_notexist = 1999
        response = self.client.put(reverse('all_books_from_collection_id', args=[book_id_notexist]), 
            data =  {
            "book_title":"Funny", 
            "author":"FFF", 
            "book_description":"NNN",
            "image":"UUU", 
            "category":"Romantic", 
            "created_by":"medved", 
            "rating": "2"
            } , content_type="application/json"
        )
        book_info = response.json()
        self.assertEqual(book_info["message"], "Book does not exist")
        self.assertEqual(response.status_code, 404)

    def test_put_404_no_user(self):
        medved = User.objects.create(username='medved')
        book= MyBook (book_title='Lucky', author='LLL', book_description='UUU', image='CCC', category='Other', created_by=medved, rating= "5",)
        book.save()
        response = self.client.put(reverse('all_books_from_collection_id', args=[book.id]), 
            data =  {
            "book_title":"Funny", 
            "author":"FFF", 
            "book_description":"NNN",
            "image":"UUU", 
            "category":"Romantic", 
            "created_by":"perina", 
            "rating": "2"
            } , content_type="application/json"
        )
        book_info = response.json()
        self.assertEqual(book_info["message"], "User does not exist")
        self.assertEqual(response.status_code, 400)
    
    def test_put_404_no_data(self):
        medved = User.objects.create(username='medved')
        book= MyBook (book_title='Lucky', author='LLL', book_description='UUU', image='CCC', category='Other', created_by=medved, rating= "5",)
        book.save()
        response = self.client.put(reverse('all_books_from_collection_id', args=[book.id]), 
            data =  { 
            "author":"FFF", 
            "book_description":"NNN",
            "image":"UUU", 
            "category":"Romantic", 
            "created_by":"perina", 
            "rating": "2"
            } , content_type="application/json"
        )
        book_info = response.json()
        self.assertEqual(book_info["message"], "Missing required data")
        self.assertEqual(response.status_code, 400)
    
    def test_put_404_no_data_1(self):
        medved = User.objects.create(username='medved')
        book= MyBook (book_title='Lucky', author='LLL', book_description='UUU', image='CCC', category='Other', created_by=medved, rating= "5",)
        book.save()
        response = self.client.put(reverse('all_books_from_collection_id', args=[book.id]))
        book_info = response.json()
        self.assertEqual(book_info["message"], "Invalid body")
        self.assertEqual(response.status_code, 400)
        
    def test_put_post(self):
        medved = User.objects.create(username='medved')
        book= MyBook (book_title='Lucky', author='LLL', book_description='UUU', image='CCC', category='Other', created_by=medved, rating= "5",)
        book.save()
        response = self.client.post(reverse('all_books_from_collection_id', args=[book.id]), 
            data =  {
            "book_title":"Funny", 
            "author":"FFF", 
            "book_description":"NNN",
            "image":"UUU", 
            "category":"Romantic", 
            "created_by":"medved", 
            "rating": "2"
            } , content_type="application/json"
        )
        book_info = response.json()
        self.assertEqual(book_info["message"], "Invalid request method")
        self.assertEqual(response.status_code, 405)












    
        


        

        

        
        
     
        
       

        

       

        
