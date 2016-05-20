from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.forms import Form
import requests
import json
from oss_main.models import Project, ProjectOwner, Issue, User, UserSkill


def index(request):
    if request.method == 'GET':
        projects = Project.objects.all().reverse()[:9]
        return render_to_response('oss_main/index.html',
                                  {'projects': projects},
                                  RequestContext(request))

    return HttpResponse(status=405)


def project_view(request, project_id):
    if request.method in ['GET','POST']:
        try:
            form = Form()
            project = ProjectOwner.objects.filter(project_id=project_id).select_related('owner__username', 'project__name')[0]
            # TODO: I will think about it. Create query to Project model like issues

            if request.method == 'POST':
                issues = Issue.objects.filter(project=project_id).all()

                r = requests.get('https://api.github.com/repos/' +
                         project.owner.username+'/'+project.project.name+'/issues?status=open')

                # If we successfully connected to current user github
                if r.status_code == 200:
                    api_result = "Successfully connected to github!"

                    github_result = json.loads(r.content)

                    for item in github_result:
                        # Get all current project names
                        current_issues_ids = [obj.github_id for obj in issues]

                        if item['id'] in current_issues_ids:
                            continue

                        # Save issue in DB
                        new_issue = Issue(
                            project = project.project,
                            name = item['title'],
                            author = project.owner, #TODO: need to create a issue User if he doesn't exist in our Project
                            url = item['html_url'],
                            github_id = item['id']
                        )
                        new_issue.save()


                else:
                    # If we can't find repos of current user in github by name
                    api_result = "Something went wrong with connection to github repo. "\
                              "Response status for user '{0}' is {1}.".format(
                                request.user, r.status_code)

            issues = Issue.objects.\
                filter(project=project_id).\
                select_related(
                'author__username',
                ).prefetch_related(
                'issueskill_set__level',
                'issueskill_set__skill',
                ).all()
            # TODO: need beautiful query ))

            for issue in issues:
                setattr(issue, 'issueskill', {})
                for item in issue._prefetched_objects_cache:
                    for obj in issue._prefetched_objects_cache[item]:
                        issue.issueskill[obj.skill.name] = obj.level.name

            return render_to_response('oss_main/project_page.html',
                                      {'form': form,
                                        'project': project,
                                        'issues': issues},
                                      RequestContext(request))

        except Project.DoesNotExist:
            raise Http404('Project not found')


def projects_list_view(request):
    if request.method == 'GET':
        # projects = Project.objects.all()
        projects = ProjectOwner.objects.select_related(
            'owner__username',
            'project__id',
            'project__name',
            'project__url',
            'project__description',
        ).all()
        return render_to_response('oss_main/projects.html',
                                  {'projects': projects},
                                  RequestContext(request))


def developers_list_view(request):
    if request.method == 'GET':
        developers = User.objects.all()
        for dev in developers:
            skills_obj = UserSkill.objects.filter(user__id=dev.pk).select_related('skill__name','level__name')
            skills = ''
            for sk in skills_obj:
                skills += sk.skill.name+'('+sk.level.name+'), '
            dev.skills = skills[:-2]
        return render_to_response('oss_main/developer.html',
                                  {'developers': developers},
                                  RequestContext(request))


def create_request(request):
    if request.method == 'GET':
        developers = User.objects.all()
        return render_to_response('oss_main/request.html',
                                  {'developers': developers},
                                  RequestContext(request))
