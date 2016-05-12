from django.conf.urls import url, include

from oss_main.views import index, projects_list_view

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^projects', projects_list_view, name='projects'),
    # url(r'^developers', , name='developers'),
<<<<<<< HEAD

    url('', include('social.apps.django_app.urls', namespace='social'))
]
=======
]
>>>>>>> 3a45c8c3e1a7bb5e308a171d04b9b926c5e4fbf0
