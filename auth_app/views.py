import json
import pdb
import requests

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages

from auth_app.forms import RegisterForm, ProfileForm


def register(request):
    form = RegisterForm(request.POST or None)

    c = RequestContext(request, {
        'form': form,
    })

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            register_form.save()
            messages.success(
                request,
                'User %s was created successful!' % request.POST['username'],
            )

            return redirect(reverse('auth_app:login'))

    return render_to_response('registration/register.html', c)


def profile(request):
    form = ProfileForm()

    _result = None

    current_context = {}
    if request.method == 'POST':
        r = requests.get(
            "https://api.github.com/users/{user}/repos".format(
                user=request.user),
        )

        if r.status_code == 200:
            _result = "Successfully connected to github!"
            current_context.update({
                'github_response': json.loads(r.content),
            })
        else:
            _result = "Something went wrong with connection to github repo. "\
                      "Response status for user '{0}' is {1}.".format(
                        request.user, r.status_code)

    current_context.update({
        'form': form,
        'result': _result,
    })

    # pdb.set_trace()

    c = RequestContext(request, current_context)

    return render_to_response('registration/profile.html', c)
