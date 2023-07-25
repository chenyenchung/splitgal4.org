from django.shortcuts import render
from django.db.models import Q
from .models import fly_line

def index(request):
    signed_in = request.user.is_authenticated
    query = request.GET.get('search-keyword')   
    if signed_in:
        see_all = request.user.is_staff
        if query:        
            line_list = fly_line.objects.filter(
                (Q(internal_sharing=see_all) |
                Q(internal_sharing=False) |
                Q(contributor=request.user.lab)|
                Q(uploader=request.user.username)) & 
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
                Q(internal_sharing=False) |
                Q(contributor=request.user.lab)|
                Q(uploader=request.user.username))
            ).order_by("id")
    else:
        if query:        
            line_list = fly_line.objects.filter(
                Q(internal_sharing=False) & 
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
                Q(internal_sharing=False)
            ).order_by("id")

    return render(request, "index.html", {
        "line_list": line_list,
        "keyword": query,
    })