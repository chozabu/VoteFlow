from models import UserExtra
from django.core.files.base import File

def save_profile_picture(backend, user, response, details,
                         is_new=False,*args,**kwargs):

    if backend.__class__.__name__ == 'FacebookOAuth2':
        up = UserExtra.objects.get_or_create(user=user) #RETURNS TUPLE (instance, created(boolean))
        if not up[0].photo:
            url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
            response = UserExtra.request.urlopen(url)
            io = UserExtra(response.read())
            up[0].photo.save('profile_pic_{}.jpg'.format(user.pk), File(io))
            up[0].save()