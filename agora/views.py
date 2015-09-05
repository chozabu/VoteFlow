from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from .forms import TopicForm


from .models import Topic, Post, Tag, Representation, PostVote, TagVote


def index(request):
	#return HttpResponse("Hello, world. You're at the agora index.")
	#'''
	#topic_list = Topic.objects
	#context = {'topic_list': topic_list}
	#return render(request, 'agora/index.html', context)
	return render(request, 'agora/index.html', {"user":user})


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
		print dir(current_topic)
		context['current_topic'] = current_topic
		if current_topic.parent:
			context['parent_topic'] = current_topic.parent
		
	return render(request, 'agora/topics.html', context)

def posts(request, topic_id, post_id):
	post = get_object_or_404(Post, pk=post_id)
	return render(request, 'agora/posts.html', {'post': post})

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
