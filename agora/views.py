from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count

from django.core import serializers

from .forms import TopicForm, PostForm, RepForm, PostVoteForm, TagForm, TagVoteForm


from django.contrib.auth.models import User
from .models import Topic, Post, Tag, Representation, PostVote, TagVote, Subscription


def index(request):
	#return HttpResponse("Hello, world. You're at the agora index.")
	#'''
	#topic_list = Topic.objects
	#context = {'topic_list': topic_list}
	#return render(request, 'agora/index.html', context)
	high_posts = Post.objects.order_by('-liquid_sum')[:5]
	recent_posts = Post.objects.order_by('-created_at')[:5]
	context = {'high_posts':high_posts,'recent_posts':recent_posts}
	return render(request, 'agora/index.html', context)
def root(request):
	#return HttpResponse("Hello, world. You're at the agora index.")
	#'''
	#topic_list = Topic.objects
	#context = {'topic_list': topic_list}
	#return render(request, 'agora/index.html', context)
	return render(request, 'agora/root.html')


def post_sankey(request, post_id, topic_id=None):
	#needs nodes - ordered list of users
	#needs links - 2xuser index and vote value
	import json
	post=Post.objects.get(pk=post_id)
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
	for v in raw_direct_votes:
		rep_list.append({
			"source": ulookup[v.author.pk],
			"target": ulookup[vals[int(v.value*2.9999)]],
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
	import json
	links=json.dumps(rep_list)

	if topic_id:
		reps = Representation.objects.filter(topic=topic_id)
		#for r in reps

	return render(request, 'agora/forcearrows.html', {"linksin":links})


def topics(request, topic_id=None, sort_method="direct_value"):
	#try:
	#	question = Question.objects.get(pk=question_id)
	#except Question.DoesNotExist:
	#	raise Http404("Question does not exist")
	#return render(request, 'agora/detail.html', {'question': question})#
	#question = get_object_or_404(Question, pk=question_id)
	topic_list = Topic.objects.filter(parent=topic_id)
	post_list = Post.objects.filter(parent=None, topic=topic_id)
	context = {'topic_list': topic_list,'post_list': post_list, "sort_method":sort_method}
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

def posts(request, topic_id, post_id, sort_method="direct_value"):
	post = get_object_or_404(Post, pk=post_id)
	topic = get_object_or_404(Topic, pk=topic_id)
	print(post)
	print(dir(post))
	#replies = Post.objects.filter(parent=post_id)
	#print dir(post)
	context={'post': post, "current_topic":topic}
	if request.user.is_authenticated():
		user_vote=PostVote.objects.filter(parent=post_id, author=request.user).first()
		context['user_vote']=user_vote
	context['sort_method']=sort_method
	return render(request, 'agora/posts.html', context)#, "replies":replies})

def view_user(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	context={'selected_user': user}
	repping = {}
	for r in user.rep_from.all():
		if r.topic not in repping:
			repping[r.topic]=[]
		repping[r.topic].append(r)
	context['repping']=repping
	
	reps = {}
	for r in user.rep_to.all():
		if r.topic not in reps:
			reps[r.topic]=[]
		reps[r.topic].append(r)
	context['reps']=reps
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

def reply_post_quick(request, topic_id, post_id, reply_type="comment"):
	# if this is a POST request we need to process the form data
	if not request.user.is_authenticated():
		print "noauth in quickvote"
		return None
	if request.method == 'POST':
		ptext = request.POST['text']
		print "QUICKREPLY", ptext
		prnt = Post.objects.get(id=post_id)
		topic = Topic.objects.get(id=topic_id)
		#TODO! CHECK topic_id == prnt.topic_id!!
		newpost = Post(subtype=reply_type, name=ptext,topic=topic, parent=prnt, author=request.user)
		newpost.save()
		return HttpResponseRedirect('/agora/topics/'+str(topic_id)+"/posts/"+str(post_id))
	return HttpResponseRedirect('/agora/topics/'+str(topic_id)+"/posts/"+str(post_id))


def vote_post_quick(request, topic_id, post_id):
	# if this is a POST request we need to process the form data
	if not request.user.is_authenticated():
		print "noauth in quickvote"
		return None
	if request.method == 'POST':
		voteval = int(request.POST['voteslider'])*.01
		print "QUICKVOTE", voteval
		vote=PostVote.objects.filter(parent=post_id, author=request.user).first()
		prnt = Post.objects.get(id=post_id)
		if vote:
			vote.value = voteval
			vote.save()
		else:
			newrep = PostVote(value=voteval, author=request.user, parent=prnt)
			newrep.save()
		prnt.count_votes()
	return HttpResponseRedirect('/agora/topics/'+str(topic_id)+"/posts/"+str(post_id))

def vote_post(request, topic_id, post_id):
	# if this is a POST request we need to process the form data
	if not request.user.is_authenticated():
		return None

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
			return HttpResponseRedirect('/agora/topics/'+str(topic_id)+"/posts/"+str(post_id))

	# if a GET (or any other method) we'll create a blank form
	else:
		form = PostVoteForm(initial={"post_id":post_id})

	return render(request, 'agora/basic_form.html', {'form': form, "action":'/agora/topics/'+str(topic_id)+"/posts/"+str(post_id)+"/vote/", "title":"vote"})

def new_post(request, parent_topic_id, parent_post_id=None):
	if not request.user.is_authenticated():
		return None
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
		return None
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
			print data['tag_name'], post.pk, request.user, post.topic.pk
			existing_tag = Tag.objects.filter(name=data['tag_name'],parent=post)
			if existing_tag:
				print "tag already found, should auto-vote on it?"#TODO
			else:
				newtag = Tag(name=data['tag_name'], parent=post, author=request.user, topic=post.topic)
				newtag.save()
			return HttpResponseRedirect('/agora/topics/'+str(topic_id)+"/posts/"+str(post.id))

	# if a GET (or any other method) we'll create a blank form
	else:
		form = TagForm(initial={"tag_name":"tag name", "post_parent_id":post_id})

	parent_topic = None
	if topic_id:
		parent_topic = Topic.objects.get(id=topic_id)

	return render(request, 'agora/basic_form.html', {
		'form': form,
		"parent_topic":parent_topic,
		"action":"/agora/topics/"+str(topic_id)+"/posts/"+str(post_id)+"/newtag/",
		"title":"Create Tag"})

def new_rep(request, parent_topic_id):
	# if this is a POST request we need to process the form data
	if not request.user.is_authenticated():
		return None
	rep=Representation.objects.filter(topic=parent_topic_id, author=request.user).first()
	if request.method == 'POST':
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
		form = RepForm(initial={"topic_id":parent_topic_id})

	parent_topic = None
	if parent_topic_id:
		parent_topic = Topic.objects.get(id=parent_topic_id)

	return render(request, 'agora/basic_form.html', {'form': form, "parent_topic":parent_topic, "action":"/agora/topics/"+str(parent_topic_id)+"/newrep", "title":"Select Representative"})

def subscribe_topic(request, parent_topic_id):
	if not request.user.is_authenticated():
		return None
	sub = Subscription.objects.filter(topic=parent_topic_id, author=request.user).first()
	if sub:
		Subscription.objects.filter(topic=parent_topic_id, author=request.user).delete()
	else:
		parent_topic=Topic.objects.get(id=parent_topic_id)
		newrep = Subscription(topic=parent_topic, author=request.user)
		newrep.save()
	return HttpResponseRedirect('/agora/topics/'+str(parent_topic_id)+"/")


def login_user(request):
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
	else:
		form = AuthenticationForm()
	return render	(request, 'agora/login.html', {'form': form})

def new_user(request):
	if request.method == "POST":
		form = UserCreationForm(data = request.POST)
		if form.is_valid():
			u = form.save()
			u.save()
			#return render(request, 'agora/index.html', {"user":u})
			return HttpResponseRedirect("/agora/login/")#, {"user":u})
			#redirect('edit_user', user_id = u.id)
	else:
		form = UserCreationForm()
	return render	(request, 'agora/newuser.html', {'form': form})
def logout_user(request):
	logout(request)
	return HttpResponseRedirect("/agora/")
