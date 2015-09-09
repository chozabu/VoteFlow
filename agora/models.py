import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

#topic
class Topic(models.Model):
	name = models.CharField(max_length=200)
	parent = models.ForeignKey("self", null = True, blank=True)
	author = models.ForeignKey(User)
	created_at = models.DateField(auto_now_add=True)
	modified_at = models.DateField(auto_now=True)

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
	def getRepresentee_links(self, voter, liquidVoted={}, results=[]):
		topic=self
		print "getRepresentee_links(", voter, ",", topic, ")"

		if self.parent:
			self.parent.getRepresentee_links(voter, liquidVoted, results)
		# print topicDict[topic]
		topicReps = Representation.objects.filter(topic=self).all()
		for links in topicReps:
			if links.author not in liquidVoted:
				if links.rep == voter:
					results.append(links)
					print("LINK:"+str(links))
					liquidVoted[links.author] = True
					if self.parent:
						self.parent.getRepresentee_links(links.author, liquidVoted, results)
		return results
	def getRepresentees(self, voter, liquidVoted={}, people=[]):
		topic=self
		print "getRepresentees(", voter, ",", topic, ")"
		topicScore = 0

		if self.parent:
			topicScore += self.parent.getRepresentees(voter, liquidVoted, people)
		# print topicDict[topic]
		topicReps = Representation.objects.filter(topic=self).all()
		for links in topicReps:
			if links.author not in liquidVoted:
				if links.rep == voter:
					people.append(links.rep)
					liquidVoted[links.author] = True
					if self.parent:
						self.parent.getRepresentees(links.author, liquidVoted, people)
		return people
	def getRepVotes(self, voter, liquidVoted={}):
		topic=self
		print "getRepVotes(", voter, ",", topic, ")"
		topicScore = 0

		if self.parent:
			topicScore += self.parent.getRepVotes(voter, liquidVoted)
		# print topicDict[topic]
		topicReps = Representation.objects.filter(topic=self).all()
		for links in topicReps:
			if links.author not in liquidVoted:
				representer = links.rep# topicReps[representee]["representer"]
				if representer == voter:
					topicScore += 1
					liquidVoted[links.author] = True
					if self.parent:
						topicScore += self.parent.getRepVotes(links.author, liquidVoted)
		return topicScore
	def __unicode__(self):
		if self.parent:
			return self.name + " @ " + str(self.parent.name)
		else:
			return self.name
#ABSTRACT - voteable
class Voteable(models.Model):
	liquid_vote_count = models.IntegerField(default=0)
	liquid_value = models.FloatField(default=0)
	direct_value = models.FloatField(default=0)
	liquid_sum = models.FloatField(default=0)
	direct_sum = models.FloatField(default=0)
	liquid_heat = models.FloatField(default=0)
	direct_heat = models.FloatField(default=0)
	created_at = models.DateField(auto_now_add=True)
	modified_at = models.DateField(auto_now=True)
	topic = models.ForeignKey(Topic)

	@property
	def liquid_value_percent(self):
		return self.liquid_value * 100.
	@property
	def direct_value_percent(self):
		return self.direct_value * 100.

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
		self.direct_sum = total
		self.direct_value = total/votelen
		liquid_value=0.0
		liquid_sum=0
		liquid_v_count = 0
		for v in votes:
			lv=self.topic.getRepVotes(v.author, voted)
			liquid_v_count+=lv
			liquid_sum += lv*v.value
		if liquid_v_count<=0:
			self.liquid_value = self.direct_value
			self.liquid_vote_count = int(votelen)
		else:
			self.liquid_value = (liquid_sum+total)/float(liquid_v_count+votelen)
			self.liquid_vote_count = int(liquid_v_count)+votelen
		self.liquid_sum = liquid_sum+total
		self.save()
	def get_liquid_voters_links(self):
		votes = PostVote.objects.filter(parent=self.id).all()
		result=[]
		voted={}
		print(votes)
		for v in votes:
			rs = []
			repes =self.topic.getRepresentee_links(v.author, voted,rs)
			#print(repes)
			#print rs
			result+=repes
		return result

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
class Tag(Voteable):
	name = models.CharField(max_length=200)
	parent = models.ForeignKey(Post)
	author = models.ForeignKey(User)
	def __unicode__(self):
		return self.name + " @ " + str(self.parent.name)

#representation
class Representation(models.Model):
	topic = models.ForeignKey(Topic)
	author = models.ForeignKey(User, related_name='rep_to')
	rep = models.ForeignKey(User, related_name='rep_from')
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
	@property
	def value_percent(self):
		return self.value * 100.
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

