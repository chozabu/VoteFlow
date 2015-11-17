from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count

from django.core import serializers

from social.apps.django_app.default.models import UserSocialAuth

from .forms import TopicForm, PostForm, RepForm, PostVoteForm, TagForm, TagVoteForm


from django.contrib.auth.models import User
from .models import Notification, Topic, Post, Tag, DGroup, \
	Representation, PostVote, TagVote, Subscription, UserRepCache, \
	GroupPermissionReq, GroupApplication, GroupMembership

import json

def home(request):
   context = RequestContext(request,
                           {'request': request,
                            'user': request.user})
   return render_to_response('agora/advlogin.html',
                             context_instance=context)

def index(request):
	context = {
		 'items':Post.objects.filter(parent=None).exclude(tag__liquid_value__gte=-.1, tag__name="completed").order_by('-liquid_heat')[:10],
		}
	return render(request, 'agora/index.html', context)

def notifications(request):

	user = request.user
	if not user.is_authenticated():
		raise Http404('Need login.')
	nlist = Notification.objects.filter(seen=False, target=user)
	if request.GET.get("markall") == "true":
		for n in nlist:
			n.seen = True
			n.save()
	return render(request, 'agora/notifications.html', {"notifications":nlist})

def root(request):
	return render(request, 'agora/root.html')

def filtertest(request):
	import html2text
	from django.core.mail import send_mail
	html_message = "testing <b> a message <br> with <i>HTML</i></b>"
	send_mail('Subject', html2text.html2text(html_message), "voteflow@gmail.com", ['chozabu@gmail.com'], fail_silently=False, html_message=html_message)
	return render(request, 'agora/posts/filtering.html')

def woi(request):
	context = {}
	context['postfilter']='{"parent":null }'
	return render(request, 'agora/posts/scatterplus.html', context=context)


#WOI API
#/agora/woi_api/?table=Post&template=api_post_list&rtype=html&sortby=-liquid_sum&startat=39
def woi_query(request):
	#r_get = request.POST
	r_get = request.GET
	print "==woiquery=="
	print r_get

	objs =Post.objects.filter()

	filters=r_get.get("filter", '[]')
	if not filters:filters="[]"
	filters=json.loads(filters)
	print filters
	for vfilter in filters:
		if not vfilter:continue
		print "@filter"
		print vfilter
		objs = objs.filter(**vfilter)

	excludes=r_get.get("exclude", '[]')
	if not excludes:excludes="[]"
	excludes=json.loads(excludes)
	print excludes
	for vexclude in excludes:
		if not vexclude:continue
		print "@exclude"
		print vexclude
		objs = objs.exclude(**vexclude)

	sortby=r_get.get("sortby")
	if sortby:
		print "@sortby"
		presort = objs
		objs = objs.order_by(sortby)
		try:
			print objs
		except:
			objs=presort


	print "@len"
	startat=int(r_get.get("startat", 0))
	length=int(r_get.get("length", 10))
	print startat, length



	#xval=r_get.get("xval", "tag__completed__liquid_sum")
	xval=r_get.get("xval", "liquid_value")
	xlist = xval.split("__")
	if xlist[0]=="tag":
		objs = objs.filter(tag__name = xlist[1] )
	
	#yval=r_get.get("xval", "tag__precise__rating")
	yval=r_get.get("yval", "liquid_sum")
	ylist = yval.split("__")
	if ylist[0]=="tag":
		objs = objs.filter(tag__name=ylist[1])


	o_count = objs.count()
	print 1
	print o_count
	objs = objs[startat:startat+length]
	print 4
	print objs
	print 5
	r_count = objs.count()
	print 3

	retr = []
	print "returning json"
	for i in objs:
		ret_obj = {"name":i.name, "id":i.id}
		if xlist[0]=="tag":
			tag=i.tag_set.filter(name=xlist[1])[0]
			ret_obj["x"] = getattr(tag, xlist[2])
		else:
			if hasattr(i, xlist[0]):
				ret_obj["x"] = getattr(i, xlist[0])
			else:
				print "no ", xlist[0]
				continue
		if ylist[0]=="tag":
			tag=i.tag_set.filter(name=ylist[1])[0]
			ret_obj["y"] = getattr(tag, ylist[2])
		else:
			if hasattr(i, ylist[0]):
				ret_obj["y"] = getattr(i, ylist[0])
			else:
				print "no ", ylist[0]
				continue
		retr.append(ret_obj)
	print retr
	return JsonResponse({"data":retr})

#basic API
#/agora/basic_api/?table=Post&template=api_post_list&rtype=html&sortby=-liquid_sum&startat=39
def db_query(request):
	if len(request.POST) == 0:
		r_get = request.GET
	else:
		r_get = request.POST
	print "==dbquery=="
	print r_get

	rdata = {"Post":Post, "Tag":Tag, "Topic":Topic, "User":User}

	table=r_get.get("table")

	if not table:
		return HttpResponse("no table")
	if table not in rdata:
		return HttpResponse("bad table")

	objs =rdata[table].objects.filter()

	filters=r_get.get("filter", '[]')
	if not filters:filters="[]"
	filters=json.loads(filters)
	print filters
	for vfilter in filters:
		if not vfilter:continue
		print "@filter"
		print vfilter
		objs = objs.filter(**vfilter)
	
	excludes=r_get.get("exclude", '[]')
	if not excludes:excludes="[]"
	excludes=json.loads(excludes)
	print excludes
	for vexclude in excludes:
		if not vexclude:continue
		print "@exclude"
		print vexclude
		objs = objs.exclude(**vexclude)

	'''exclude=r_get.get("exclude")
	if exclude:
		print "@exclude"
		ve = json.loads(exclude)
		print ve
		objs = objs.exclude(**ve)'''

	sortby=r_get.get("sortby")
	if sortby:
		print "@sortby"
		presort = objs
		objs = objs.order_by(sortby)
		try:
			print objs
		except:
			objs=presort


	print "@len"
	startat=int(r_get.get("startat", 0))
	length=int(r_get.get("length", 10))
	print startat, length

	o_count = objs.count()
	print 1
	print o_count
	objs = objs[startat:startat+length]
	print 4
	print objs
	print 5
	r_count = objs.count()
	print 3

	print "@type"
	rtype=r_get.get("rtype")
	if rtype=="html":
		print "returning html", len(objs)
		context = {table:objs, "total_num":o_count, "got_num":r_count, "start_at":startat}
		if sortby:
			if sortby[0]=="-":sortby=sortby[1:]#TODO allow reverse sorting in API!!
			context['sort_method']=sortby
		return render(request, 'agora/' + r_get.get("template") + '.html', context)

	retr = []
	print "returning json"
	fields=r_get.getlist("fields", ['pk','id'])
	print fields
	for i in objs:
		ret_obj = {}
		for f in fields:
			ret_obj[f] = getattr(i, f)
		retr.append(ret_obj)
	return HttpResponse(json.dumps(retr))

def search(request):
	r_get = request.GET
	print "==search=="
	print r_get
	searchtext=r_get.get("searchtext", "")
	context = {'searchtext':searchtext}
	if searchtext:
		post_list = Post.objects.filter(name__icontains =searchtext)[0:10]

		context['post_list']=post_list
	return render(request, 'agora/search.html', context)




def post_sankey(request, post_id):
	#needs nodes - ordered list of users
	#needs links - 2xuser index and vote value
	#foos = Foo.objects.all()
	#data = serializers.serialize('json', foos)
	#raw_topic_list = Topic.objects.all()#filter(parent=topic_id)
	ulookup = {}
	user_list = []
	rep_list = []
	uindex = 0
	ulookup["mid"]= uindex
	user_list.append({"name": "mid"})
	uindex+=1
	ulookup["low"]= uindex
	user_list.append({"name": "low"})
	uindex+=1
	ulookup["high"]= uindex
	user_list.append({"name": "high"})
	uindex+=1

	liquidvoted = {}

	post=Post.objects.get(pk=post_id)
	print "POST:", post
	raw_link_list = post.get_liquid_voters_links()
	for r in raw_link_list:
		print r
		if r.author.pk not in ulookup:
			ulookup[r.author.pk]= uindex
			user_list.append({
				"name": r.author.username
			})
			uindex+=1
		if r.rep.pk not in ulookup:
			ulookup[r.rep.pk]= uindex
			user_list.append({
				"name": r.rep.username
			})
			uindex+=1

	raw_direct_votes = PostVote.objects.filter(parent=post.id).all()
	vals = ["low", "mid", "high"]
	print(raw_direct_votes)
	print(vals)
	for v in raw_direct_votes:
		if v.author.pk not in ulookup:
			ulookup[v.author.pk]= uindex
			user_list.append({
				"name": v.author.username
			})
			uindex+=1
		liquidvoted[v.author] = True

	if post.topic:
		for v in raw_direct_votes:
			rep_list.append({
				"source": ulookup[v.author.pk],
				"target": ulookup[vals[int((v.value*.5+.5)*2.9999)]],
				"value": post.topic.getRepVotes(v.author,dict(liquidvoted))+1
			})
		for r in raw_link_list:
			if r.author not in liquidvoted:#ulookup[r.author.pk] != ulookup[r.rep.pk]:
				rep_list.append({
					"source": ulookup[r.author.pk],
					"target": ulookup[r.rep.pk],
					"value": post.topic.getRepVotes(r.author,dict(liquidvoted))+1
				})
				#print(rep_list[-1]["value"])
	else:
		for v in raw_direct_votes:
			rep_list.append({
				"source": ulookup[v.author.pk],
				"target": ulookup[vals[int((v.value*.5+.5)*2.9999)]],
				"value": 1
			})



	nodes=json.dumps(user_list)
	links=json.dumps(rep_list)
	#print(raw_link_list)
	#print(rep_list)
	context = {"linksin":links,"nodesin":nodes}#, "rrlinks":raw_link_list}
	current_topic = post.topic
	context['current_topic'] = current_topic
	context['post'] = post
	return render(request, 'agora/sankey.html', context)
def topic_forcearrows(request, topic_id=None):
	#foos = Foo.objects.all()
	#data = serializers.serialize('json', foos)
	#raw_topic_list = Topic.objects.all()#filter(parent=topic_id)
	raw_rep_list = Representation.objects.all()
	rep_list = []
	ltypes = ["suit", "licensing", "resolved"]
	for r in raw_rep_list:
		rep_list.append({
			"source": r.author.username,
			"target": r.rep.username,
			"type": ltypes[len(r.topic.name)%3]
		})
	links=json.dumps(rep_list)

	if topic_id:
		reps = Representation.objects.filter(topic=topic_id)
		#for r in reps

	return render(request, 'agora/forcearrows.html', {"linksin":links})
def topic_sunburst(request, topic_id=None):
	topic_list = Topic.objects.filter(parent=topic_id)
	root = {"name":"Topics", "children":[]}
	children = root['children']
	def sbrecur(tc, cin):
		subtopics = tc.topic_set.all()
		cin.append({
			"name": "",
			"size": tc.post_set.count()
		})
		for t in subtopics:
			c=[]
			cin.append({
				"name": t.name,
				"children": c
			})
			sbrecur(t, c)
	for t in topic_list:
		c = []
		children.append({
			"name": t.name,
			"children": c
		})
		sbrecur(t, c)
	rootin=json.dumps(root)

	return render(request, 'agora/sunburst.html', {"rootin":rootin})


def topics(request, topic_id=None, sort_method="liquid_value"):
	topic_list = Topic.objects.filter(parent=topic_id)
	post_list = Post.objects.filter(parent=None, topic=topic_id).exclude(tag__liquid_value__gte=-.1, tag__name="completed")[0:10]
	context = {'topic_list': topic_list,'post_list': post_list, "sort_method":sort_method}
	context['postfilter']='{"topic":'+str(topic_id)+', "parent":null }'
	if topic_id:
		current_topic = Topic.objects.get(id=topic_id)
		context['current_topic'] = current_topic
		if request.user.is_authenticated():
			rep = Representation.objects.filter(topic=topic_id, author=request.user).first()
			if rep: context['rep'] = rep
			print "representitive:", rep
			sub = Subscription.objects.filter(topic=topic_id, author=request.user).first()
			if sub: context['sub'] = sub
		print dir(current_topic)
		if current_topic.parent:
			context['parent_topic'] = current_topic.parent
		
	return render(request, 'agora/topics.html', context)

def groups(request):
	group_list = DGroup.objects.filter(parent=None)
	context = {'group_list': group_list}
	return render(request, 'agora/all_groups.html', context)

def group(request, group_id, sort_method="liquid_value"):
	group = get_object_or_404(DGroup, pk=group_id)
	context = {'group': group, "sort_method":sort_method}
	membership=None
	pending_membership=None
	if request.user.is_authenticated():
		pending_membership = GroupApplication.objects.filter(group=group, author=request.user).first()
		membership = GroupMembership.objects.filter(group=group, author=request.user).first()
	if membership:
		context['membership']=membership
	if pending_membership:
		context['pending_membership']=pending_membership
	context['postfilter']='{"group":'+str(group_id)+', "parent":null }'
	context['group_list'] = DGroup.objects.filter(parent=group)
	context['post_list'] = Post.objects.filter(parent=None, group=group).exclude(tag__liquid_value__gte=-.1, tag__name="completed")[0:10]
	print context
	return render(request, 'agora/group.html', context)


def fancy_group(request, group_id=None):
	group_id = request.GET.get('group_id', group_id)
	group = DGroup.objects.filter(pk=group_id)
	context = {}
	if group:
		context['group'] = group[0]
	return render(request, 'agora/fancy_group.html', context)#, "replies":replies})

def group_members(request, group_id):
	#group_id = request.GET.get('group_id', group_id)
	group = DGroup.objects.get(pk=group_id)
	context = {'group':group}
	return render(request, 'agora/groups/members_list.html', context)#, "replies":replies})

def group_member_setlevel_submit(request, group_id):
	# if this is a POST request we need to process the form data
	if not request.user.is_authenticated():
		print "noauth in newgroup"

		return HttpResponseRedirect("/agora/login/")
	if request.method == 'POST':
		group = DGroup.objects.get(pk=group_id)
		print request.POST
		permission, reason = group.user_has_permission(request.user, "edit_member_levels")
		if not permission:return HttpResponse(reason)
		userid=request.POST.get("userid")
		level=float(request.POST.get("level"))
		membership = GroupMembership.objects.filter(group=group,author_id=userid).first()
		if membership:
			membership.level=level
			membership.save()
	return HttpResponseRedirect('/agora/groups/'+str(group_id)+'/members/')



def group_pending_member_answer(request, group_id, user_id, rtype):
	if not request.user.is_authenticated():
		print "noauth in approve pending group member"
		return HttpResponseRedirect("/agora/login")
	group = DGroup.objects.get(pk=group_id)
	permission, reason = group.user_has_permission(request.user, "approve_application")
	if not permission:return HttpResponse(reason)
	application = GroupApplication.objects.get(group=group, author_id=user_id)
	if int(rtype)==1:
		membership = GroupMembership(group=group, author=application.author)
		membership.save()
		print membership
	GroupApplication.objects.get(group=group, author_id=user_id).delete()
	context = {'group':group}
	return HttpResponseRedirect('/agora/groups/'+str(group_id)+'/pending_members/')

def group_pending_members(request, group_id):
	#group_id = request.GET.get('group_id', group_id)
	group = DGroup.objects.get(pk=group_id)
	context = {'group':group}
	return render(request, 'agora/groups/pending_members_list.html', context)#, "replies":replies})

def group_rules(request, group_id):
	#group_id = request.GET.get('group_id', group_id)
	group = DGroup.objects.get(pk=group_id)
	context = {'group':group}
	return render(request, 'agora/groups/rules_list.html', context)#, "replies":replies})
def group_rules_quick(request,group_id):
	# if this is a POST request we need to process the form data
	if not request.user.is_authenticated():
		print "noauth in newgroup"
		return HttpResponseRedirect("/agora/login")
	if request.method == 'POST':
		group = DGroup.objects.get(pk=group_id)
		permission, reason = group.user_has_permission(request.user, "edit_rules")
		if not permission:return HttpResponse(reason)
		rule_name=request.POST.get("rule")
		rule_level=float(request.POST.get("level"))
		rules = GroupPermissionReq.objects.filter(name=rule_name,group=group)
		if rules:
			rule=rules[0]
			rule.author=request.user
		else:
			rule=GroupPermissionReq(name=rule_name,group=group, author=request.user)
		rule.level=rule_level
		rule.save()
	return HttpResponseRedirect('/agora/groups/'+str(group_id)+'/rules/')

def join_group(request, group_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/agora/login")

	if request.method != 'POST':
		return HttpResponse("Error. Complain about this!")
	membership = GroupMembership.objects.filter(group_id=group_id, author=request.user).first()
	application = GroupApplication.objects.filter(group_id=group_id, author=request.user).first()
	group = DGroup.objects.get(pk=group_id)
	if membership or application:
		GroupMembership.objects.filter(group=group, author=request.user).delete()
		GroupApplication.objects.filter(group=group, author=request.user).delete()
	else:
		if group.subtype == "public":
			membership = GroupMembership(group=group, author=request.user)
			membership.save()
		else:
			application = GroupApplication(group=group, author=request.user)
			application.save()
		#TODO send notifications to members who can approve
	return HttpResponseRedirect('/agora/groups/'+str(group_id)+"/")


def group_quick(request,group_id=None):
	# if this is a POST request we need to process the form data
	if not request.user.is_authenticated():
		print "noauth in newgroup"
		return HttpResponseRedirect("/agora/login")
	if request.method == 'POST':
		print request.POST
		parent_id=request.POST.get("group_id", None)
		if parent_id:
			print "---parent_id---"
			print parent_id
			parent_id = int(parent_id)
			parent_group = DGroup.objects.get(id=parent_id)
			rule_check = GroupPermissionReq.objects.get(group=parent_group, name="add_subgroup")
			own_membership = GroupMembership.objects.filter(group=parent_group, author=request.user).first()
			if not own_membership:
				return HttpResponse("Access denied. You need to join the group.")
			if own_membership.level < rule_check.level:
				return HttpResponse("Access denied. You need to be at least level" + str(rule_check.level) + " but you are level" + str(own_membership.level))

		ptext = request.POST['text']
		btext = request.POST.get('body_text', '')
		print "btext=",btext
		subtype = request.POST['subtype']
		#btext = request.POST.get('body_text', '')
		print "fancy_group", ptext
		newgroup = DGroup(name=ptext, text=btext, author=request.user, subtype=subtype)
		if parent_id:#could validate this..
			newgroup.parent = parent_group
		newgroup.save()
		gms = GroupMembership(group=newgroup, author=request.user,level=100)
		gms.save()
		GroupPermissionReq(name="add_post", group=newgroup, author=request.user,level=1).save()
		GroupPermissionReq(name="add_subgroup", group=newgroup, author=request.user,level=5).save()
		GroupPermissionReq(name="approve_application", group=newgroup, author=request.user,level=10).save()
		GroupPermissionReq(name="edit_rules", group=newgroup, author=request.user,level=30).save()
		GroupPermissionReq(name="edit_member_levels", group=newgroup, author=request.user,level=30).save()
		if group_id==None:
			group_id=newgroup.id
		return HttpResponseRedirect('/agora/groups/'+str(group_id))
	return HttpResponseRedirect('/agora/groups/'+str(group_id))



def all_topics(request, sort_method="subscription_set"):
	topic_list = []
	if sort_method == "subscription_set":
		topic_list = Topic.objects.filter(parent=None) \
	            .annotate(num_subscription=Count('subscription')) \
	            .order_by('-num_subscription')
	elif sort_method == "post_set":
		topic_list = Topic.objects.filter(parent=None) \
	            .annotate(num_post=Count('post')) \
	            .order_by('-num_post')
	else:
		topic_list = Topic.objects.filter(parent=None)
	context = {'topic_list': topic_list, "sort_method":sort_method}

	if "all_topics" in request.get_full_path():
		context['recur']=True
		context['tpage']="all_topics"
	else:
		context['tpage']="topics"

	return render(request, 'agora/all_topics.html', context)

def posts(request, post_id, sort_method="direct_value"):
	post = get_object_or_404(Post, pk=post_id)
	topic = post.topic
	context={'post': post, "current_topic":topic}
	if request.user.is_authenticated():
		user_vote=PostVote.objects.filter(parent=post_id, author=request.user).first()
		context['user_vote']=user_vote
	context['sort_method']=sort_method
	return render(request, 'agora/posts.html', context)#, "replies":replies})

def tags(request, tag_id):
	tag = get_object_or_404(Tag, pk=tag_id)
	post = tag.parent
	topic = tag.topic
	context={'post': post, 'tag': tag, "current_topic":topic}
	if request.user.is_authenticated():
		user_vote=TagVote.objects.filter(parent=tag_id, author=request.user).first()
		context['user_vote']=user_vote
	return render(request, 'agora/tags.html', context)#, "replies":replies})

def alltags(request, tag_word):
	#cfil['tag__liquid_value__gte'] = -.1;
	#cfil['tag__name'] = "completed";
	posts = Post.objects.filter(tag__name=tag_word)
	context={'posts': posts, 'tag_word': tag_word}
	#if request.user.is_authenticated():
	#	user_vote=TagVote.objects.filter(parent=tag_id, author=request.user).first()
	#	context['user_vote']=user_vote
	return render(request, 'agora/alltags.html', context)#, "replies":replies})

def fancy_post(request):
	parent_id = request.GET.get("parent_id", None)
	topic_id = request.GET.get("topic_id", None)
	group_id = request.GET.get("group_id", None)
	print topic_id
	context={}
	if parent_id:
		parent = Post.objects.get(pk=parent_id)
		context['parent'] = parent
	if topic_id:
		topic = Topic.objects.get(pk=topic_id)
		context['topic'] = topic
		context['current_topic'] = topic
		print topic
	if group_id:
		group = DGroup.objects.get(pk=group_id)
		context['group'] = group

	return render(request, 'agora/fancy_post.html', context)#, "replies":replies})
from compare_user import compareusers
def view_user(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	context={'selected_user': user}

	repping = {}
	for r in user.rep_from.all():
		if r.topic not in repping:
			cache = UserRepCache.objects.get_or_create(user=user, topic=r.topic)[0]
			repping[r.topic]={"cache":cache,"people":[]}
		repping[r.topic]['people'].append(r)
	context['repping']=repping
	
	reps = {}
	for r in user.rep_to.all():
		if r.topic not in reps:
			reps[r.topic]=[]
		reps[r.topic].append(r)
	context['reps']=reps

	if request.user.is_authenticated():
		if user==request.user:
			context['own_profile'] = True
			context['fb_ss'] = UserSocialAuth.objects.filter(user=request.user, provider="facebook")
			context['goog_ss'] = UserSocialAuth.objects.filter(user=request.user, provider="google-oauth2")
		else:
			usr_cmp = compareusers(user,request.user)
			if usr_cmp:
				context['similarity'] = usr_cmp[0]
				context['compared_vote_count'] = usr_cmp[2]
	return render(request, 'agora/user.html', context)#, "replies":replies})

def view_users(request):
	users = User.objects.filter(is_active=True)
	context={'users': users}
	return render(request, 'agora/users.html', context)#, "replies":replies})

def new_topic(request, parent_topic_id=None):
	# if this is a POST request we need to process the form data
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/agora/topics/'+str(parent_topic_id))
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = TopicForm(request.POST)
		# check whether it's valid:
		print form
		if form.is_valid():
			data = form.cleaned_data
			newtopic = Topic(name=data['topic_name'],parent=data['topic_parent_id'],author=request.user)
			newtopic.save()
			subs = Subscription(topic=newtopic, author=request.user)
			subs.save()
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			print newtopic
			print newtopic.id
			print '/agora/topics/'+str(newtopic.id)
			return HttpResponseRedirect('/agora/topics/'+str(newtopic.id))

	# if a GET (or any other method) we'll create a blank form
	else:
		form = TopicForm(initial={"topic_name":"topic name",  "topic_parent_id":parent_topic_id})
		
	parent_topic = None
	if parent_topic_id:
		parent_topic = Topic.objects.get(id=parent_topic_id)

	return render(request, 'agora/newtopic.html', {'form': form, "parent_topic":parent_topic})

def post_quick(request, post_id=None, reply_type="comment"):
	topic_id=None
	# if this is a POST request we need to process the form data
	group_id = None
	if not request.user.is_authenticated():
		print "noauth in quickvote"
		return HttpResponseRedirect("/agora/login")
	if request.method == 'POST':
		tid = request.POST.get('topic_id', topic_id)
		if tid: topic_id = tid
		pid = request.POST.get('post_id', post_id)
		if pid: post_id = pid
		gid = request.POST.get('group_id', group_id)
		if gid: group_id = gid
	if topic_id==None and post_id==None and group_id==None:
		return HttpResponse("Need Post, group or topic ID"+str(group_id))
	prnt = None
	if post_id!=None:
		prnt = Post.objects.get(id=post_id)
		topic_id=prnt.topic_id
		group_id=prnt.group_id
	if request.method == 'POST':
		ptext = request.POST['text']
		btext = request.POST.get('body_text', '')
		reply_type = request.POST.get('subtype', reply_type)
		print "FANCY_REPLY", ptext, btext
		print "reply type:", reply_type
		print request.POST
		print "topic_id: ", topic_id
		#topic = Topic.objects.get(id=topic_id)
		if group_id != None:
			parent_group = DGroup.objects.get(id=group_id)
			rule_check = GroupPermissionReq.objects.get(group=parent_group, name="add_post")
			own_membership = GroupMembership.objects.filter(group=parent_group, author=request.user).first()
			if not own_membership:
				return HttpResponse("Access denied. You need to join the group.")
			if own_membership.level < rule_check.level:
				return HttpResponse("Access denied. You need to be at least level" + str(rule_check.level) + " but you are level" + str(own_membership.level))

		newpost = Post(text=btext, subtype=reply_type, name=ptext,topic_id=topic_id, group_id=group_id, parent=prnt, author=request.user)
		newpost.save()
		if post_id==None:
			post_id=newpost.id
		#this could be in an override on post save?
		if prnt:
			newnotify = Notification(target=prnt.author, name="New Post", content_object=newpost, author=request.user)
			newnotify.save()
		if newpost.topic:
			for subs in newpost.topic.subscription_set.all():
				newnotify = Notification(target=subs.author, name="New Post", content_object=newpost, author=request.user)
				newnotify.save()
		if newpost.group:
			for user in newpost.group.members:
				newnotify = Notification(target=user, name="New Post", content_object=newpost, author=request.user)
				newnotify.save()
		return HttpResponseRedirect("/agora/posts/"+str(post_id))
	return HttpResponseRedirect("/agora/posts/"+str(post_id))

def reply_post_quick(request, topic_id, post_id, reply_type="comment"):
	# if this is a POST request we need to process the form data
	if not request.user.is_authenticated():
		print "noauth in quickvote"
		return HttpResponseRedirect("/agora/login")
	if request.method == 'POST':
		ptext = request.POST['text']
		print "QUICKREPLY", ptext
		prnt = Post.objects.get(id=post_id)
		topic = Topic.objects.get(id=topic_id)
		#TODO! CHECK topic_id == prnt.topic_id!!
		newpost = Post(subtype=reply_type, name=ptext,topic=topic, parent=prnt, author=request.user)
		newpost.save()
		#this could be in an override on post save?
		if prnt:
			newnotify = Notification(target=prnt.author, name="New Post", content_object=newpost, author=request.user)
			newnotify.save()
		return HttpResponseRedirect('/agora/topics/'+str(topic_id)+"/posts/"+str(post_id))
	return HttpResponseRedirect('/agora/topics/'+str(topic_id)+"/posts/"+str(post_id))

def votepost(vote, prnt, user, voteval):
	if vote:
		vote.value = voteval
		vote.save()
		nprefix = "New"
	else:
		vote = PostVote(value=voteval, author=user, parent=prnt)
		vote.save()
		nprefix = "Updated"
	prnt.count_votes()
	newnotify = Notification(target=prnt.author, name=nprefix+" vote on your post", content_object=vote, author=vote.author)
	newnotify.save()

def vote_post_quick(request, post_id):
	# if this is a POST request we need to process the form data
	if not request.user.is_authenticated():
		print "noauth in quick post"
		return HttpResponseRedirect("/agora/login")
	if request.method == 'POST':
		#covert (0 ... 100) to (-1 ... 1)
		voteval = float(request.POST['voteslider'])*.02-1.
		print "QUICKVOTE", voteval
		vote=PostVote.objects.filter(parent=post_id, author=request.user).first()
		prnt = Post.objects.get(id=post_id)
		votepost(vote, prnt, request.user, voteval)
	return HttpResponseRedirect("/agora/posts/"+str(post_id))


def unvote_post_quick(request, post_id):
	# if this is a POST request we need to process the form data
	if not request.user.is_authenticated():
		print "noauth in unvote"
		return HttpResponseRedirect("/agora/login")
	PostVote.objects.filter(parent=post_id, author=request.user).delete()
	prnt = Post.objects.get(id=post_id)
	prnt.count_votes()
	return HttpResponseRedirect("/agora/posts/"+str(post_id))

def vote_tag_quick(request, tag_id):
	# if this is a POST request we need to process the form data
	if not request.user.is_authenticated():
		print "noauth in quick tag"
		return HttpResponseRedirect("/agora/login")
	if request.method == 'POST':
		#covert (0 ... 100) to (-1 ... 1)
		voteval = float(request.POST['voteslider'])*.02-1.
		print "QUICKTAGVOTE", voteval
		vote=TagVote.objects.filter(parent=tag_id, author=request.user).first()
		prnt = Tag.objects.get(id=tag_id)
		if vote:
			vote.value = voteval
			vote.save()
		else:
			newrep = TagVote(value=voteval, author=request.user, parent=prnt)
			newrep.save()
		prnt.count_votes(TagVote)
	return HttpResponseRedirect('/agora/tags/'+str(tag_id))

def vote_post(request, post_id):
	# if this is a POST request we need to process the form data
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/agora/login")

	if request.method == 'POST':
		form = PostVoteForm(request.POST)
		print form
		if form.is_valid():
			data = form.cleaned_data
			prnt = Post.objects.get(id=post_id)
			vote=PostVote.objects.filter(parent=post_id, author=request.user).first()
			if vote:
				vote.value = data['value']
				vote.save()
			else:

				newrep = PostVote(value=data['value'], author=request.user, parent=prnt)
				newrep.save()
			prnt.count_votes()
			return HttpResponseRedirect('/agora/posts/'+str(post_id))

	# if a GET (or any other method) we'll create a blank form
	else:
		form = PostVoteForm(initial={"post_id":post_id})

	return render(request, 'agora/basic_form.html', {'form': form, "action":'/agora/topics/'+str(topic_id)+"/posts/"+str(post_id)+"/vote/", "title":"vote"})

def new_post(request, parent_topic_id, parent_post_id=None):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/agora/login")
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		form = PostForm(request.POST)
		print form
		if form.is_valid():
			data = form.cleaned_data
			newpost = Post(name=data['post_name'],topic=data['topic_id'], parent=data['post_parent_id'], author=request.user)
			newpost.save()
			return HttpResponseRedirect('/agora/topics/'+str(parent_topic_id)+"/posts/"+str(newpost.id))

	# if a GET (or any other method) we'll create a blank form
	else:
		form = PostForm(initial={"post_name":"post name", "post_parent_id":parent_post_id, "topic_id":parent_topic_id})
		
	parent_topic = None
	if parent_topic_id:
		parent_topic = Topic.objects.get(id=parent_topic_id)

	return render(request, 'agora/basic_form.html', {'form': form, "parent_topic":parent_topic, "action":"/agora/topics/"+str(parent_topic_id)+"/newpost/", "title":"Create Post"})

def new_tag(request, post_id, topic_id=None):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/agora/login")
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		form = TagForm(request.POST)
		#print "---"
		#print request.POST
		#print form.cleaned_data
		print "---"
		if form.is_valid():
			data = form.cleaned_data
			post = get_object_or_404(Post, pk=data['post_parent_id'].id)
			print data['tag_name'], post.pk, request.user
			existing_tag = Tag.objects.filter(name=data['tag_name'],parent=post)
			if existing_tag:
				print "tag already found, should auto-vote on it?"#TODO
			else:
				newtag = Tag(name=data['tag_name'], parent=post, author=request.user, topic=post.topic)
				newtag.save()
			return HttpResponseRedirect('/agora/posts/'+str(post.id))

	# if a GET (or any other method) we'll create a blank form
	else:
		form = TagForm(initial={"tag_name":"tag name", "post_parent_id":post_id})

	parent_topic = None
	if topic_id:
		parent_topic = Topic.objects.get(id=topic_id)

	return render(request, 'agora/basic_form.html', {
		'form': form,
		"parent_topic":parent_topic,
		"action":"/agora/posts/"+str(post_id)+"/newtag/",
		"title":"Create Tag"})

def new_rep(request, parent_topic_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/agora/login")
	rep=Representation.objects.filter(topic=parent_topic_id, author=request.user).first()
	parent_topic = Topic.objects.get(id=parent_topic_id)
	context = {"current_topic":parent_topic}
	if rep: context['current_rep']=rep
	return render(request, 'agora/new_rep.html', context)
def confirm_rep(request, parent_topic_id,rep_id):
	parent_topic = Topic.objects.get(id=parent_topic_id)
	new_rep = User.objects.get(id=rep_id)
	#return render(request, 'agora/new_rep.html', {"parent_topic":parent_topic, "action":"/agora/topics/"+str(parent_topic_id)+"/newrep", "title":"Select Representative"})

	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		if not request.user.is_authenticated():
			return HttpResponseRedirect("/agora/login")
		rep=Representation.objects.filter(topic=parent_topic_id, author=request.user).first()
		form = RepForm(request.POST)
		print form
		if form.is_valid():
			data = form.cleaned_data
			if rep:
				rep.topic = data['topic_id']#unneeded? should check instead
				rep.rep=data['representative_id']
				rep.save()
			else:
				newrep = Representation(topic=data['topic_id'], rep=data['representative_id'], author=request.user)
				newrep.save()
			return HttpResponseRedirect('/agora/topics/'+str(parent_topic_id)+"/")

	# if a GET (or any other method) we'll create a blank form
	else:
		return render(request, 'agora/new_rep_confirm.html', {"current_topic":parent_topic, "rep":new_rep})
		#form = RepForm(initial={"topic_id":parent_topic_id})

	parent_topic = None
	if parent_topic_id:
		parent_topic = Topic.objects.get(id=parent_topic_id)

	return render(request, 'agora/basic_form.html', {'form': form, "parent_topic":parent_topic, "action":"/agora/topics/"+str(parent_topic_id)+"/newrep", "title":"Select Representative"})

def subscribe_topic(request, parent_topic_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/agora/login")
	if request.method != "POST": return HttpResponse("this method should be POST")
	sub = Subscription.objects.filter(topic=parent_topic_id, author=request.user).first()
	if sub:
		Subscription.objects.filter(topic=parent_topic_id, author=request.user).delete()
	else:
		parent_topic=Topic.objects.get(id=parent_topic_id)
		newrep = Subscription(topic=parent_topic, author=request.user)
		newrep.save()
	return HttpResponseRedirect('/agora/topics/'+str(parent_topic_id)+"/")


def login_user(request):
	print dir(request)
	if request.method == "POST":
		form = AuthenticationForm(data = request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			print "user:", user
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(request.POST['nexturl'])
					# Redirect to a success page.
				else:
					# Return a 'disabled account' error message
					#...
					pass
			else:
				# Return an 'invalid login' error message.
				#...
				pass
			#u = form.save()
			#u.save()
			#return render(request, 'agora/index.html', {"user":u})
			return HttpResponseRedirect("/agora/")#, {"user":user})
			#redirect('edit_user', user_id = u.id)
	'''
	/agora/login/ :{;{ request.path }}
	/agora/login/?next=asd: {;{ request.get_full_path }}
	http://lc.lan:8000/agora/: {;{ request.META.HTTP_REFERER }}
	lc.lan:8000: {;{ request.META.HTTP_HOST }}
	asd: {;{ request.GET.next }}
	'''
	print request.META
	next= request.META['HTTP_HOST']+request.get_full_path()
	if 'HTTP_REFERER' in request.META:
		if request.META['HTTP_REFERER'][7:].startswith(request.META['HTTP_HOST']):
			next = request.META['HTTP_REFERER']

	form = AuthenticationForm()
	import requests
	context = {'form': form, 'next':next}
	'''if request.user.is_authenticated():
		user = request.user
		social = user.social_auth.get(provider='google-oauth2')
		response = requests.get(
		    'https://www.googleapis.com/plus/v1/people/me/people/visible',
		    params={'access_token': social.extra_data['access_token']}
		)
		friends = response.json()
		context['friends']=friends'''
	return render	(request, 'agora/login.html', context)

def new_user(request):
	raise Http404('Disabled for now - use FB or Google login!')
	'''if request.method == "POST":
		form = UserCreationForm(data = request.POST)
		if form.is_valid():
			u = form.save()
			u.save()
			#return render(request, 'agora/index.html', {"user":u})
			return HttpResponseRedirect("/agora/login/")#, {"user":u})
			#redirect('edit_user', user_id = u.id)
	else:
		form = UserCreationForm()
	return render	(request, 'agora/newuser.html', {'form': form})'''
def logout_user(request):
	logout(request)
	return HttpResponseRedirect("/agora/login")
