from django.conf.urls import url

from oss_main.views import index

urlpatterns = [
    url(r'^', index, name='index'),
]