from django.contrib import admin

from network.models import Followers, posts, Likes, User

# Register your models here.
admin.site.register(Followers)
admin.site.register(User)
admin.site.register(posts)
admin.site.register(Likes)