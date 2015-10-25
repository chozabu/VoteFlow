import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.functions import Length

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.html import escape

class UserExtra(models.Model):
	user = models.OneToOneField(User)
	photo = models.ImageField(null=True, blank=True)
	def image_url(self):
		"""
		Returns the URL of the image associated with this Object.
		If an image hasn't been uploaded yet, it returns a stock image

		:returns: str -- the image url

		"""
		if self.photo and hasattr(self.photo, 'url'):
			return self.photo.url
		else:
			return '/static/agora/img/default_profile_pic.png'
	@property
	def unseen_notifications(self):
		return self.user.notifications.filter(seen=False)
	@property
	def seen_notifications(self):
		return self.user.notifications.filter(seen=True)


@receiver(post_save, sender=User)
def create_user_extra(sender, instance, created, **kwargs):
	if created:
		UserExtra.objects.create(user=instance)


class DGroup(models.Model):
	name = models.CharField(max_length=80)
	text = models.TextField(default="")
	author = models.ForeignKey(User, null=True, blank=True)
	parent = models.ForeignKey("DGroup", null=True, blank=True, related_name='children')
	subtype = models.CharField(max_length=20, default="public")
	created_at = models.DateField(auto_now_add=True)
	modified_at = models.DateField(auto_now=True)
	hidden = models.BooleanField(default=False)
	@property
	def safetext(self):
		return escape(self.text)
	def path(self):
		list = []
		cur_top = self.parent
		print "top:",cur_top
		while cur_top:
			list.append(cur_top)
			if cur_top.parent:
				cur_top=cur_top.parent
			else:cur_top=None
		list.reverse()
		return list
	def full_path(self):
		list = []
		cur_top = self
		print "---"
		while cur_top:
			print cur_top
			list.append(cur_top)
			if cur_top.parent:
				cur_top=cur_top.parent
			else:cur_top=None
		print "==="
		list.reverse()
		return list
	@property
	def members(self):
		return User.objects.filter(group_memberships__group=self)
	@property
	def pending_members(self):
		return User.objects.filter(group_applications__group=self)
	def user_has_permission(self, user, permission):
		own_membership = GroupMembership.objects.filter(group=self, author=user).first()
		if not own_membership: return False, "not a member of this group " + self.name
		rule_check = GroupPermissionReq.objects.filter(group=self, name=permission).first()
		if not rule_check: return False, "rule" + str(permission) + " does not exist in " + self.name
		if own_membership.level >= rule_check.level:
			return True, "Membership level higher than Rule"
		return False, "You don't have Permission to " + str(permission) + " in " + self.name


'''@receiver(post_save, sender=Group)
def create_group_extra(sender, instance, created, **kwargs):
	if created:
		GroupExtra.objects.create(group=instance)'''


class GroupPermissionReq(models.Model):
	name = models.CharField(max_length=200)
	group = models.ForeignKey(DGroup, related_name='permission_reqs')
	author = models.ForeignKey(User)
	created_at = models.DateField(auto_now_add=True)
	modified_at = models.DateField(auto_now=True)
	level = models.FloatField(default=1)
	def __unicode__(self):
		return str(self.name) + "(+"+str(self.level)+")"
class GroupMembership(models.Model):
	group = models.ForeignKey(DGroup, related_name='memberships')
	author = models.ForeignKey(User, related_name='group_memberships')
	created_at = models.DateField(auto_now_add=True)
	modified_at = models.DateField(auto_now=True)
	level = models.FloatField(default=1)
	def __unicode__(self):
		return str(self.author) + "(+"+str(self.level)+")@"+self.group.name
class GroupApplication(models.Model):
	group = models.ForeignKey(DGroup, related_name='applications')
	author = models.ForeignKey(User, related_name='group_applications')
	created_at = models.DateField(auto_now_add=True)
	modified_at = models.DateField(auto_now=True)
	def __unicode__(self):
		return str(self.author) +"@"+self.group.name

class Notification(models.Model):
	name = models.CharField(max_length=200, null=True, blank=True)
	#url = models.CharField(max_length=200, null=True, blank=True)#perhaps a link?
	target = models.ForeignKey(User, related_name='notifications')
	seen = models.BooleanField(default=False)
	author = models.ForeignKey(User, null=True, blank=True, related_name='notifications_generated')
	content_type = models.ForeignKey(ContentType, null=True, blank=True)
	object_id = models.PositiveIntegerField(null=True, blank=True)
	content_object = GenericForeignKey('content_type', 'object_id')
	def __unicode__(self):
		return self.name + " from " + self.author.username + " about " + str(self.content_object)

#topic
class Topic(models.Model):
	name = models.CharField(max_length=200)
	parent = models.ForeignKey("self", null = True, blank=True)
	author = models.ForeignKey(User)
	created_at = models.DateField(auto_now_add=True)
	modified_at = models.DateField(auto_now=True)

	@property
	def sorted_subs(self):
		return self.topic_set.order_by(Length('subscription').desc())
	@property
	def num_followers(self):
		return self.topic_set.count()
		#liquid votes
		#for each vote author
			#get list of reps in topics to root
	def path(self):
		list = []
		cur_top = self.parent
		while cur_top:
			list.append(cur_top)
			cur_top=cur_top.parent
		list.reverse()
		return list
	def full_path(self):
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
	def getRepVotes(self, voter, liquidVoted={}, notify=None):
		topic=self
		print "getRepVotes(", voter, ",", topic, ")"
		topicScore = 0

		if self.parent:
			topicScore += self.parent.getRepVotes(voter, liquidVoted, notify=notify)
		# print topicDict[topic]
		topicReps = Representation.objects.filter(topic=self).all()
		for links in topicReps:
			if links.author not in liquidVoted:
				representer = links.rep# topicReps[representee]["representer"]
				if representer == voter:
					topicScore += 1
					liquidVoted[links.author] = True
					if notify:
						newnotify = Notification(target=links.author, name="Representative Voted!!", content_object=notify, author=voter)
						newnotify.save()
					if self.parent:
						topicScore += self.parent.getRepVotes(links.author, liquidVoted, notify=notify)
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
	topic = models.ForeignKey(Topic, null = True, blank=True)

	@property
	def liquid_value_percent(self):
		return self.liquid_value * 50. + 50.
	@property
	def direct_value_percent(self):
		return self.direct_value * 50. + 50.

	def count_votes(self, table=None):
		if table==None:
			table=PostVote
		print "======counting votes======"
		nowtime = datetime.date.today()
		#direct votes
		votes = table.objects.filter(parent=self.id).all()
		total = 0.0
		heat = 0.0
		voted={}
		for v in votes:
			total+=v.value
			heat += (v.value)/((nowtime-v.created_at).days*0.1+1.)
			voted[v.author]=True
			print v.value
		votelen=len(votes)
		self.direct_sum = total
		self.direct_heat = total
		if votelen:
			self.direct_value = total/votelen
		else:
			self.direct_value =0
			self.direct_sum = 0
			self.liquid_value=0
			self.liquid_sum=0
			self.liquid_vote_count=0
		#liquid_value=0.0
		liquid_sum=0
		liquid_heat=0
		liquid_v_count = 0
		if self.topic:
			for v in votes:
				lv=self.topic.getRepVotes(v.author, voted, notify=v)
				liquid_v_count+=lv
				liquid_sum += lv*v.value
				liquid_heat += (lv*v.value)/((nowtime-v.created_at).days*0.1+1.)
		if liquid_v_count<=0:
			self.liquid_value = self.direct_value
			self.liquid_vote_count = int(votelen)
		else:
			print liquid_sum,total,liquid_v_count,votelen
			self.liquid_value = (liquid_sum+total)/float(liquid_v_count+votelen)
			self.liquid_vote_count = int(liquid_v_count)+votelen
		self.liquid_sum = liquid_sum+total
		self.liquid_heat = liquid_heat+heat
		print liquid_sum, total
		print "liquid heat: ", self.liquid_heat
		print "heat: ", heat
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
	subtype = models.CharField(max_length=20, default="comment")
	text = models.TextField(default="")
	group = models.ForeignKey(DGroup, null = True, blank=True)
	@property
	def safetext(self):
		return escape(self.text)
	@property
	def path(self):
		list = []
		cur_top=self.parent
		while cur_top:
			list.append(cur_top)
			cur_top=cur_top.parent
		list.reverse()
		return list
	@property
	def full_path(self):
		list = [self]
		cur_top=self.parent
		while cur_top:
			list.append(cur_top)
			cur_top=cur_top.parent
		list.reverse()
		return list
	@property
	def get_comments(self):
		return self.post_set.filter(subtype='comment')
	@property
	def get_options(self):
		return self.post_set.filter(subtype='option')
	@property
	def get_concerns(self):
		return self.post_set.filter(subtype='concern')
	@property
	def get_benefits(self):
		return self.post_set.filter(subtype='benefit')
	@property
	def get_polls(self):
		return self.post_set.filter(subtype='poll')
	@property
	def get_proposals(self):
		return self.post_set.filter(subtype='proposal')
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
	def cache_rep_info(self):
		uc = UserRepCache.objects.get_or_create(user=self.rep, topic=self.topic)[0]
		print uc
		uc.cache_rep_info(self)
	def __unicode__(self):
		return self.author.username + " -> " + self.rep.username + " @ " + str(self.topic.name)

class UserRepCache(models.Model):
	user = models.ForeignKey(User, related_name='rep_cache')
	topic = models.ForeignKey(Topic)
	rep_cache = models.IntegerField(default=1)
	def cache_rep_info(self, rfrom=None):
		#cval = self.rep_cache
		topicReps = Representation.objects.filter(topic=self.topic, rep=self.user)
		newval = 1
		for tr in topicReps:
			if tr == rfrom:continue
			if tr.author==rfrom.rep and tr.rep == rfrom.author: continue
			uci = UserRepCache.objects.get_or_create(user=tr.author, topic=self.topic)[0]
			newval+=uci.rep_cache
			print newval
		if newval != self.rep_cache:
			#this has been changed
			self.rep_cache = newval
			self.save()
			#update objects it is pointing to
			topicReps = Representation.objects.filter(topic=self.topic, author=self.user)
			for tr in topicReps:
				if tr == rfrom:continue
				if tr.author==rfrom.rep and tr.rep == rfrom.author: continue
				#this could be optimised by altering from the diff in value
				tr.cache_rep_info()
	def __unicode__(self):
		return self.user.username + " = " + str(self.rep_cache) + " @ " + str(self.topic.name)


@receiver(post_save, sender=Representation)
def update_rep_data(sender, instance, created, **kwargs):
	instance.cache_rep_info()
	#if created:
	#	UserExtra.objects.create(user=instance)

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
		return self.value * 50. + 50.
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

