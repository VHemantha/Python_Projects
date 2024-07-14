from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.title, name="title"),
    path("search/", views.search , name="search"),
    path("NewPage/", views.newpage, name="newPage"),
    path("/editpage/", views.editpage, name="EditPage"),
    path("saveedit/", views.saveedit, name="saveedit"),
    path("random/", views.random_page, name="random")
]
