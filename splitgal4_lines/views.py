from django.http import HttpResponse
from django.template import loader
from .models import fly_line

def index(request):
    line_list = fly_line.objects.filter(internal_sharing=False).order_by("id")
    template = loader.get_template("index.html")
    context = {
        "line_list": line_list,
    }
    return HttpResponse(template.render(context, request))