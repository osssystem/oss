from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from oss_main.models import Project


def index(request):
    if request.method == 'GET':
        projects = Project.objects.all().reverse()[:9]
        return render_to_response('oss_main/index.html', projects)

    return HttpResponse(status=405)


def project_view(request, project_id):
    if request.method == 'GET':
        try:
            project = Project.objects.get(id=project_id)
            http = 'Project: '+project.name+'<br> Link: '+project.url
            HttpResponse(http)

        except Project.DoesNotExist:
            raise Http404('Project not found')


def projects_list_view(request):
    if request.method == 'GET':
        projects = Project.objects.all()

        # What's that?
        # http= ''
        # for item in project:
        #     http = http+ item.id+' / '+item.name+' / '+item.url+'<br>'

        return render_to_response('oss_main/projects.html', {
                'projects': projects
            })




def developers_list_view(request):
    pass