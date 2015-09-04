import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

#topic
class Topic(models.Model):
	name = models.CharField(max_length=200)
	parent = models.ForeignKey("self", null = True, blank=True)
	author = models.ForeignKey(User)
	def __unicode__(self): 
		if self.parent:
			return self.name + " @ " + str(self.parent.name)
		else:
			return self.name

#post
class Post(models.Model):
	name = models.CharField(max_length=200)
	parent = models.ForeignKey("self", null = True, blank=True)
	author = models.ForeignKey(User)
	topic = models.ForeignKey(Topic)
	def __unicode__(self): 
		return self.name

#tag
class Tag(models.Model):
	name = models.CharField(max_length=200)
	parent = models.ForeignKey(Post)
	author = models.ForeignKey(User)
	def __unicode__(self): 
		return self.name + " @ " + str(self.parent.name)

#representation
class Representation(models.Model):
	name = models.CharField(max_length=200)
	topic = models.ForeignKey(Topic)
	author = models.ForeignKey(User, related_name='author')
	rep = models.ForeignKey(User, related_name='rep')
	def __unicode__(self): 
		return self.author.username + " -> " + self.rep.username + " @ " + str(self.topic.name)

#post vote
class PostVote(models.Model):
	value = models.FloatField(default=0)
	parent = models.ForeignKey(Post)
	author = models.ForeignKey(User)
	def __unicode__(self): 
		return self.author.username + " : " + str(self.value) + "@" + self.parent.name[0:20]
#tag vote
class TagVote(models.Model):
	value = models.FloatField(default=0)
	parent = models.ForeignKey(Tag)
	author = models.ForeignKey(User)
	def __unicode__(self): 
		return self.author.username + " : " + str(self.value) + "@" + self.parent.name[0:20]

