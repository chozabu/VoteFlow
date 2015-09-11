from django import forms

from .models import Topic, Post, Tag, Representation, PostVote, TagVote
from django.contrib.auth.models import User

class TopicForm(forms.Form):
	topic_parent_id = forms.ModelChoiceField(label='Parent Topic', queryset = Topic.objects.all(),required=False)
	topic_name = forms.CharField(label='Topic Name', max_length=100)
    

class PostForm(forms.Form):
	topic_id = forms.ModelChoiceField(label='Parent Topic', queryset = Topic.objects.all())
	post_parent_id = forms.ModelChoiceField(label='Parent Post', queryset = Post.objects.all(),required=False)
	post_name = forms.CharField(label='Message', max_length=100)

class PostVoteForm(forms.Form):
	post_id = forms.ModelChoiceField(label='Parent',queryset = Post.objects.all())
	value = forms.FloatField(label='Vote (between -1 and 1, eg: .5)', max_value=1, min_value=-1)

class TagForm(forms.Form):
	post_parent_id = forms.ModelChoiceField(label='Parent Post', queryset = Post.objects.all(),required=False)
	tag_name = forms.CharField(label='Tag', max_length=100)

class TagVoteForm(forms.Form):
	tag_id = forms.ModelChoiceField(label='Tag',queryset = Tag.objects.all())
	value = forms.FloatField(label='Vote (between 0 and 1, eg: .5)', max_value=1, min_value=0)

class RepForm(forms.Form):
	topic_id = forms.ModelChoiceField(label='Topic', queryset = Topic.objects.all())
	representative_id = forms.ModelChoiceField(label='Representitive', queryset = User.objects.all())


