from django.conf.urls import url, include
from django.contrib.auth.views import login, logout, logout_then_login
# temp imports
from oss_main.views import index
from auth_app.views import register

urlpatterns = [
    url(r'^login/', login,
        name='login',
        ),
    url(r'^logout/',
        logout,
        # logout_then_login,
        name='logout'
        ),
    # temp index
    url(r'^user_profile', index, name='user_profile'),
    url(r'^register', register, name='register'),
]
