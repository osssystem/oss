from django.conf.urls import url

from oss_main.views import index,projects_list_view

urlpatterns = [
    url(r'^', index, name='index'),
    url('projects',projects_list_view,name = 'projects'),
]