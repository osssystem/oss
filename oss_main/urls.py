from django.conf.urls import url, include

from oss_main.views import index, projects_list_view, developers_list_view, create_request

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^projects', projects_list_view, name='projects'),
    url(r'^developers', developers_list_view, name='developers'),
    url(r'^request', create_request, name='request'),
]