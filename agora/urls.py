 
from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /agora/
    url(r'^$', views.index, name='index'),
    # ex: /agora/topics/
    url(r'^topics/$', views.topics, name='topics'),
    # ex: /agora/topics/5/
    url(r'^topics/(?P<topic_id>[0-9]+)/$', views.topics, name='topics'),
    # ex: /agora/topics/5/posts/5/
    url(r'^topics/(?P<topic_id>[0-9]+)/posts/(?P<post_id>[0-9]+)$', views.posts, name='posts'),
    # ex: /agora/5/vote/
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]