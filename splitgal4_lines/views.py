from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import fly_line


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    line_list = fly_line.objects.filter(internal_sharing=False).order_by("id")
    template = loader.get_template("index.html")
    context = {
        "line_list": line_list,
    }
    # output = ", ".join([q.gene_name for q in line_list])
    return HttpResponse(template.render(context, request))