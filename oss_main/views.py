from django.http import HttpResponse
from django.shortcuts import render_to_response


def index(request):
    if request.method == 'GET':
        return render_to_response('oss_main/index.html')
    return HttpResponse(status=405)
