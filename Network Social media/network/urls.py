
from unicodedata import name
from django.urls import path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("network/<str:profilename>", views.profile, name="profile"),
    path("follower", views.follower, name="follower"),

    #API Routes
    path("updatepost", views.updatepost, name="update"),
    path("updatelikes", views.updatelikes, name="updatelikes")
]
urlpatterns += staticfiles_urlpatterns()