from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from oss_main.models import Project, ProjectOwner, Issue, User


def index(request):
    if request.method == 'GET':
        projects = Project.objects.all().reverse()[:9]
        return render_to_response('oss_main/index.html',
                                  {'projects': projects},
                                  RequestContext(request))

    return HttpResponse(status=405)


def project_view(request, project_id):
    if request.method == 'GET':
        try:
            project = ProjectOwner.objects.select_related().get(project_id=project_id)
            # TODO: I will think about it. Create query to Project model like issues

            issues = Issue.objects.\
                filter(project=project_id).\
                select_related(
                'author__username',
                ).prefetch_related(
                'issueskill_set__level',
                'issueskill_set__skill',
                ).all()
            # TODO: need butifull query ))

            for issue in issues:
                setattr(issue, 'issueskill', {})
                for item in issue._prefetched_objects_cache:
                    for obj in issue._prefetched_objects_cache[item]:
                        issue.issueskill[obj.skill.name] = obj.level.name

            return render_to_response('oss_main/project_page.html',
                                      {'project': project,
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
        return render_to_response('oss_main/developer.html',
                                  {'developers': developers},
                                  RequestContext(request))


def create_request(request):
    if request.method == 'GET':
        developers = User.objects.all()
        return render_to_response('oss_main/request.html',
                                  {'developers': developers},
                                  RequestContext(request))
