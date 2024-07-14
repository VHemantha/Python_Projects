from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Followers, Likes, User, posts
import json


def index(request):
    if request.method == 'POST':
        newpost = request.POST["newpost"]
        user = User.objects.get(id = request.user.id)
        foo = posts(user_id=user, post=newpost, like=0)
        foo.save()
        bar = posts.objects.all().order_by('-time')
        paginator = Paginator(bar,10)
        pagenumber = request.GET.get('page')
        page_obj = paginator.get_page(pagenumber)
        return render(request, "network/index.html",{
            "post_data":page_obj
        })
    bar = posts.objects.all().order_by('-time')
    paginator = Paginator(bar,10)
    pagenumber = request.GET.get('page')
    page_obj = paginator.get_page(pagenumber)
    return render(request, "network/index.html",{
        "post_data":page_obj
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, profilename):

    if request.method == 'POST':
        if 'follow' in request.POST:
            user = User.objects.get(id = request.user.id)   
            foo = Followers(user=user,follower=profilename)
            foo.save()
        if 'unfollow' in request.POST:
            delrecord = Followers.objects.filter(follower = profilename)
            delrecord.delete()
    bar=Followers.objects.values().all()
    fols_count = Followers.objects.filter(user__username = profilename).count()
    fows_count = Followers.objects.filter(follower = profilename).count()
    namecheck = 1
    for i in range(len(bar)):
        if bar[i]["follower"] == profilename:
            namecheck = 0
    user = User.objects.get(id = request.user.id)
    baz = posts.objects.filter(user_id= user).order_by('-time')
    paginator = Paginator(baz,10)
    pagenumber = request.GET.get('page')
    page_obj = paginator.get_page(pagenumber)
    return render(request, "network/profile.html",{
        "myposts":page_obj,
        "profilename":profilename,
        "namec":namecheck,
        "folws": fols_count,
        "folwer": fows_count
    })


def follower(request):
    foo = Followers.objects.values().filter(user = request.user.id)
    bar = posts.objects.values().all().order_by('-time')
    baz = User.objects.values().all()
    ids = []
    post = []
    for i in range(len(foo)):
        for j in range(len(baz)):
            if foo[i]["follower"] == baz[j]["username"]:
                list = {}
                list["id"] = baz[j]["id"]
                list["username"] = baz[j]["username"]
                ids.append(list)
    for i in range(len(ids)):
        for j in range(len(bar)):             
            list={}
            if ids[i]["id"] == bar[j]["user_id_id"]:
                list["post"] = bar[j]["post"]
                list["user_id"] = ids[i]["username"]
                list["time"] = bar[j]["time"]         
                post.append(list)
    paginator = Paginator(post,10)
    pagenumber = request.GET.get('page')
    page_obj = paginator.get_page(pagenumber)
    return render(request, "network/follower.html",{
        "fol_post":page_obj
    })    

@csrf_exempt
@login_required
def updatepost(request):
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        post = posts.objects.get(user_id = request.user, pk = data["id"])
        if data.get("post") is not None:
            post.post = data["post"]
        post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


@csrf_exempt
@login_required
def updatelikes(request):
    if request.method == 'PUT':
        data = json.loads(request.body)

        post = posts.objects.get(user_id = request.user, pk = data["id"])
        if data.get("like") is not None:
            post.like = data["like"]
            post.save()
        return HttpResponse(status=204)

