__author__ = 'chozabu'

from models import PostVote, User

def compare_all_users():
	users = User.objects.all()
	usercount = users.count()
	print usercount
	for ui in range(usercount-1):
		u=users[ui]
		for ui2 in range(ui+1, usercount):
			u2 = users[ui2]
			usrcmp = compareusers(u,u2)
			if usrcmp:
				print u, u2, compareusers(u,u2)

def compareusers(a,b, topic=None):
	#get all votes by a on an item b also voted on
	va = PostVote.objects.filter(author=a, parent__postvote__author=b).order_by('parent')
	#and the reverse
	vb = PostVote.objects.filter(author=b, parent__postvote__author=a).order_by('parent')
	count = va.count()
	if count == 0: return None
	tdiff = 0
	#get cumlitiave difference between votes
	for x in range(count):
		ia = va[x]
		ib = vb[x]
		diff = abs(ia.value-ib.value)
		tdiff+=diff
	#convert to percent
	rdiff=100-(tdiff/count*50.)
	return rdiff,tdiff,count
	#UserCompare(a,b,rdiff,tdiff,count)
