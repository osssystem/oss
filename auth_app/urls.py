from django.conf.urls import url, include
from django.contrib.auth.views import login, logout

from auth_app.views import register, profile, get_user_info

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
    url(r'^user_profile', profile, name='user_profile'),
    url(r'^register', register, name='register'),
    url(r'^get_user_info', get_user_info, name='get_user_info'),

]
