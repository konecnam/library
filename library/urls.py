from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("best_sellers", views.best_sellers, name="best_sellers"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    # path("more_info_a_book/<str:category>", views.more_info_a_book, name="more_info_a_book"),
    path("more_info_a_book/<str:category>/<str:number>", views.more_info_a_book, name="more_info_a_book"),
    path('upload/', views.upload_file, name='upload_file'),
    path('collection', views.collection, name='collection')
]
