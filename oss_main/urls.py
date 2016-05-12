from django.conf.urls import url, include

from oss_main.views import index,projects_list_view

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^projects', projects_list_view, name='projects'),
    # url(r'^developers', , name='developers'),

    url('', include('social.apps.django_app.urls', namespace='social'))
]