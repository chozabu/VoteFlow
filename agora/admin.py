from django.contrib import admin

# Register your models here.
from .models import Topic, Post, Tag, Representation, PostVote, TagVote


admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Representation)
admin.site.register(PostVote)
admin.site.register(TagVote)
