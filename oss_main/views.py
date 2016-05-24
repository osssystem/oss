from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.forms import Form
import requests
import json
from oss_main.models import Project, Issue, User, UserSkill, IssueSkill


def index(request):
    if request.method == 'GET':
        projects = Project.objects.all().reverse()[:9]
        return render_to_response('oss_main/index.html',
                                  {'projects': projects},
                                  RequestContext(request))

    return HttpResponse(status=405)


def project_view(request, project_id):
    if request.method in ['GET', 'POST']:
        try:
            form = Form()

            project = Project.objects.prefetch_related('owner__owner').get(id=project_id)
            setattr(project, 'owners', {})
            for item in project._prefetched_objects_cache['owner']:
                project.owners[item._owner_cache.username] = item._owner_cache.git_url

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
    if request.method in ['GET', 'POST']:
        if request.method == 'GET':
            projects = Project.objects.prefetch_related(
                'issue_set__issueskill_set__skill',
                'issue_set__issueskill_set__level',
                'owner__owner',
            ).all()

            for project in projects:
                setattr(project, 'projectskills', {})
                for item in project._prefetched_objects_cache['issue']:
                    for skills in item._prefetched_objects_cache['issueskill']:
                        project.projectskills[skills.skill.name] = skills.level.name

            for project in projects:
                setattr(project, 'owners', {})
                for item in project._prefetched_objects_cache['owner']:
                    project.owners[item._owner_cache.username] = item._owner_cache.git_url

            return render_to_response('oss_main/projects.html',
                                      {'projects': projects},
                                      RequestContext(request))

        elif request.method == 'POST':
            try:
                skills = UserSkill.objects.filter(user=request.user.id)
                search_result = []
                for skill in skills:
                    projects_temp = IssueSkill.objects.filter(
                        skill_id=skill.skill_id,
                        level_id__in=[skill.level_id, str(skill.level_id+1)],).values('issue__project_id')

                    for item in projects_temp:
                        if item['issue__project_id'] not in search_result:
                            search_result.append(item['issue__project_id'])

                projects = Project.objects.filter(
                    id__in=search_result).prefetch_related(
                    'issue_set__issueskill_set__skill',
                    'issue_set__issueskill_set__level',
                    'owner__owner',
                )

                for project in projects:
                    setattr(project, 'projectskills', {})
                    for item in project._prefetched_objects_cache['issue']:
                        for skills in item._prefetched_objects_cache['issueskill']:
                            project.projectskills[skills.skill.name] = skills.level.name

                for project in projects:
                    setattr(project, 'owners', {})
                    for item in project._prefetched_objects_cache['owner']:
                        project.owners[item._owner_cache.git_url] = item._owner_cache.username

                return render_to_response('oss_main/projects.html',
                                          {'projects': projects},
                                          RequestContext(request))

            except UserSkill.DoesNotExist:
                raise Http404('Skills not found')


def developers_list_view(request):
    if request.method == 'GET':
        developers = User.objects.all()
        for dev in developers:
            skills_obj = UserSkill.objects.filter(user__id=dev.pk).select_related('skill__name', 'level__name')
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
