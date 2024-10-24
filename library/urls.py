from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("best_sellers", views.best_sellers, name="best_sellers"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("more_info_a_book/<str:category>/<str:number>", views.more_info_a_book, name="more_info_a_book"),
    path('upload/', views.upload_file, name='upload_file'),
    path('collection', views.collection, name='collection'), 
    path('delete', views.delete, name='delete'),
    path('collection_edit/<str:book_id>', views.collection_edit, name='collection_edit'), 
    path('collection_edit_upload', views.collection_edit_upload, name='collection_edit_upload'),
    path('add_collection_form_book', views.add_collection_form, name='add_collection_form_book'), 
    path('delete_upload_file', views.delete_upload_file, name='delete_upload_file'),
    path ('stars', views.stars, name='stars'),
]
