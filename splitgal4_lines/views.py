from django.http import HttpResponse
from django.template import loader
from django.db.models import Q
from .models import fly_line

def index(request):
    see_all = request.user.is_staff
    query = request.GET.get('search-keyword')   
    if query:        
        line_list = fly_line.objects.filter(
            (Q(internal_sharing=see_all) |
             Q(internal_sharing=False)) & 
            (
                Q(gene_name__icontains=query) |
                Q(effector_type__icontains=query) |
                Q(activator_type__icontains=query) |
                Q(cassette__icontains=query) |
                Q(contributor__icontains=query)|
                Q(reference__icontains=query)
            )
        ).order_by("id")
    else:
        line_list = fly_line.objects.filter(
            (Q(internal_sharing=see_all) |
             Q(internal_sharing=False))
        ).order_by("id")

    template = loader.get_template("index.html")
    context = {
        "line_list": line_list,
    }

    return HttpResponse(template.render(context, request))