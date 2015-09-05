from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from .forms import TopicForm, PostForm, RepForm, PostVoteForm


from .models import Topic, Post, Tag, Representation, PostVote, TagVote, Subscription


def index(request):
	#return HttpResponse("Hello, world. You're at the agora index.")
	#'''
	#topic_list = Topic.objects
	#context = {'topic_list': topic_list}
	#return render(request, 'agora/index.html', context)
	return render(request, 'agora/index.html')


def topics(request, topic_id=None):
	#try:
	#	question = Question.objects.get(pk=question_id)
	#except Question.DoesNotExist:
	#	raise Http404("Question does not exist")
	#return render(request, 'agora/detail.html', {'question': question})#
	#question = get_object_or_404(Question, pk=question_id)
	topic_list = Topic.objects.filter(parent=topic_id)
	context = {'topic_list': topic_list}
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

def posts(request, topic_id, post_id):
	post = get_object_or_404(Post, pk=post_id)
	topic = get_object_or_404(Topic, pk=topic_id)
	#replies = Post.objects.filter(parent=post_id)
	#print dir(post)
	return render(request, 'agora/posts.html', {'post': post, "current_topic":topic})#, "replies":replies})

def new_topic(request, parent_topic_id=None):
	# if this is a POST request we need to process the form data
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

def new_post(request, parent_topic_id, parent_post_id=None):
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

def new_rep(request, parent_topic_id):
	# if this is a POST request we need to process the form data
	if not request.user.is_authenticated():
		return None
	rep=Subscription.objects.filter(topic=parent_topic_id, author=request.user).first()
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
			return HttpResponseRedirect("/agora/")#, {"user":u})
			#redirect('edit_user', user_id = u.id)
	else:
		form = UserCreationForm()
	return render	(request, 'agora/newuser.html', {'form': form})
def logout_user(request):
	logout(request)
	return HttpResponseRedirect("/agora/")
