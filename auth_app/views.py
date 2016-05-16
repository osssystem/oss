import json
import pdb
import requests

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages
from django.db import transaction
from django.http import Http404

from auth_app.forms import RegisterForm, ProfileForm
from oss_main.models import Project, ProjectOwner


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
    if not request.user.is_authenticated():
        raise Http404("No such page.")

    form = ProfileForm()
    api_result = None

    # Get all projects for current user
    current_projects = Project.objects.filter(projectowner__owner=request.user)

    # Initialize current context with projects
    current_context = {"projects": current_projects, }

    # If we click on our button
    if request.method == 'POST':
        r = requests.get(
            "https://api.github.com/users/{user}/repos".format(
                user=request.user),
        )

        # If we successfully connected to current user github
        if r.status_code == 200:
            api_result = "Successfully connected to github!"

            github_result = json.loads(r.content)

            # Here we will accumulate newly created projects
            saved_projects = []

            for project in github_result:
                # Get all current project names
                current_projects_names = [obj.name for obj in current_projects]

                if project['name'] in current_projects_names:
                    continue

                # Save project in DB
                with transaction.atomic():
                    new_project = Project(
                        name=project['name'],
                        url=project['html_url'],
                        description=project['description']
                    )
                    new_project.save()

                    owner = ProjectOwner(
                        project=new_project,
                        owner=request.user
                    )
                    owner.save()

                    saved_projects.append(new_project)

            # If we got some new projects
            if len(saved_projects) > 0:
                api_result += " %s new project added!" % len(saved_projects)
                current_context.update({
                    'saved_projects': saved_projects,
                })
            else:
                api_result += " But there are no new projects here!"
        else:
            # If we can't find repos of current user in github by name
            api_result = "Something went wrong with connection to github repo. "\
                      "Response status for user '{0}' is {1}.".format(
                        request.user, r.status_code)

    current_context.update({
        'form': form,
        'api_result': api_result,
    })
    c = RequestContext(request, current_context)

    return render_to_response('registration/profile.html', c)
