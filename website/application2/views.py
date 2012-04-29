from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, Http404
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from application2.models import Model1, Model2

def home(request):
    return HttpResponse("you have come home to app2")

def get_id(request):
    id = request.REQUEST['id']
    try:
        posting_obj = Model1.objects.get(x = id)
    except Exception:
        return HttpResponse("you have no entry with x = " + id)
    return HttpResponse("your request id was there " + id)
