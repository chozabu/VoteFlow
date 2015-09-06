import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

#topic
class Topic(models.Model):
	name = models.CharField(max_length=200)
	parent = models.ForeignKey("self", null = True, blank=True)
	author = models.ForeignKey(User)

		#liquid votes
		#for each vote author
			#get list of reps in topics to root
	def path(self):
		list = []
		cur_top = self
		while cur_top:
			list.append(cur_top)
			cur_top=cur_top.parent
		list.reverse()
		return list
	def getRepVotes(self, voter, liquidVoted={}):
		topic=self
		print "getRepVotes(", voter, ",", topic, ")"
		topicScore = 0

		if self.parent:
			topicScore += self.parent.getRepVotes(voter, liquidVoted)
		# print topicDict[topic]
		topicReps = Representation.objects.filter(topic=self).all()
		for representee in topicReps:
			if representee.author not in liquidVoted:
				representer = representee.rep# topicReps[representee]["representer"]
				if representer == voter:
					topicScore += 1
					liquidVoted[representee.author] = True
					if self.parent:
						topicScore += self.parent.getRepVotes(representee.author, liquidVoted)
		return topicScore
	def __unicode__(self):
		if self.parent:
			return self.name + " @ " + str(self.parent.name)
		else:
			return self.name
#ABSTRACT - voteable
class Voteable(models.Model):
	liquid_value = models.FloatField(default=0)
	direct_value = models.FloatField(default=0)
	liquid_heat = models.FloatField(default=0)
	direct_heat = models.FloatField(default=0)
	created_at = models.DateField(auto_now_add=True)
	modified_at = models.DateField(auto_now=True)
	topic = models.ForeignKey(Topic)

	def count_votes(self):
		print "======counting votes======"
		#direct votes
		votes = PostVote.objects.filter(parent=self.id).all()
		total = 0.0
		voted={}
		for v in votes:
			total+=v.value
			voted[v.author]=True
		votelen=len(votes)
		self.direct_value = total/votelen
		liquid_value=total
		for v in votes:
			print self
			lv=self.topic.getRepVotes(v.author, voted)
			liquid_value += lv*v.value
		self.liquid_value = liquid_value
		self.save()


	class Meta:
		abstract = True

#post
class Post(Voteable):
	name = models.CharField(max_length=200)
	parent = models.ForeignKey("self", null = True, blank=True)
	author = models.ForeignKey(User)
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
	topic = models.ForeignKey(Topic)
	author = models.ForeignKey(User, related_name='author')
	rep = models.ForeignKey(User, related_name='rep')
	def __unicode__(self):
		return self.author.username + " -> " + self.rep.username + " @ " + str(self.topic.name)

#Topic Subscription
class Subscription(models.Model):
	topic = models.ForeignKey(Topic)
	author = models.ForeignKey(User)
	def __unicode__(self):
		return self.author.username + " @ " + str(self.topic.name)

#post vote
class MetaVote(models.Model):
	value = models.FloatField(default=0)
	author = models.ForeignKey(User)
	created_at = models.DateField(auto_now_add=True)
	modified_at = models.DateField(auto_now=True)
	def __unicode__(self):
		return self.author.username + " : " + str(self.value) + "@" + self.parent.name[0:20]

	class Meta:
		abstract = True
#post vote
class PostVote(MetaVote):
	parent = models.ForeignKey(Post)
#tag vote
class TagVote(MetaVote):
	parent = models.ForeignKey(Tag)

