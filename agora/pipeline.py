from models import UserExtra
from django.core.files.base import File
import urllib2 as urllib
from io import BytesIO

def save_profile_picture(backend, user, response, details,
                         is_new=False,*args,**kwargs):

    if backend.__class__.__name__ == 'FacebookOAuth2':
        up = UserExtra.objects.get_or_create(user=user) #RETURNS TUPLE (instance, created(boolean))
        if not up[0].photo:
            url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
            print url
            response = urllib.urlopen(url)
            io = BytesIO(response.read())
            up[0].photo.save('ppics/profile_pic_{}.jpg'.format(user.pk), File(io))
            up[0].save()
