from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from models import Project

def index(request):
    if request.method == 'GET':
        http = '''Wecome to OSS sytem <br>
        latest projects <br>
        1. NeuralNetworks
        2. SimpleManagement
        3. BestLua
        '''


        return HttpResponse(http)
    #        return render_to_response('oss_main/index.html')

    return HttpResponse(status=405)

def project(request,project_id):
    if request.method == 'GET':
        try:
            project = Project.objects.get(id = project_id)
            http = 'Project: '+Project.name+'<br> Link: '+Project.url
            HttpResponse(http)

        except Project.DoesNotExist:
            raise Http404('Project not found')



