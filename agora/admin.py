from django.contrib import admin

# Register your models here.
from .models import UserRepCache, UserExtra, DGroup, Notification, Topic, Post, Tag, Representation, PostVote, TagVote, Subscription


admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Representation)
admin.site.register(PostVote)
admin.site.register(TagVote)
admin.site.register(Subscription)
admin.site.register(Notification)
admin.site.register(UserExtra)
admin.site.register(DGroup)
admin.site.register(UserRepCache)
