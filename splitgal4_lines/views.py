from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from .models import fly_line
from .forms import RemoveLineForm
from upload.forms import NewLineForm

def index(request):
    signed_in = request.user.is_authenticated
    query = request.GET.get('search-keyword') 
    if signed_in:
        see_all = request.user.contributor
        if query:        
            line_list = fly_line.objects.filter(
                Q(removed=False) &
                (Q(private=see_all) |
                Q(private=False) |
                Q(contributor=request.user.lab)|
                Q(uploader=request.user)) & 
                (
                    Q(gene_name__icontains=query) |
                    Q(effector_type__icontains=query) |
                    Q(source_id__icontains=query) |
                    Q(cassette__icontains=query) |
                    Q(contributor__icontains=query)|
                    Q(citation__icontains=query)
                )
            ).order_by("status", "-date_created")
        else:
            line_list = fly_line.objects.filter(
                Q(removed=False) &
                (Q(private=see_all) |
                Q(private=False) |
                Q(contributor=request.user.lab)|
                Q(uploader=request.user))
            ).order_by("status", "-date_created")
    else:
        if query:        
            line_list = fly_line.objects.filter(
                Q(removed=False) &
                Q(private=False) & 
                (
                    Q(gene_name__icontains=query) |
                    Q(effector_type__icontains=query) |
                    Q(cassette__icontains=query) |
                    Q(source_id__icontains=query) |
                    Q(contributor__icontains=query)|
                    Q(citation__icontains=query)
                )
            ).order_by("id")
        else:
            line_list = fly_line.objects.filter(
                Q(removed=False) &
                Q(private=False)
            ).order_by("id")

    return render(request, "index.html", {
        "line_list": line_list,
        "keyword": query,
    })
    
def idv_line(request, sg_id):
    sgline = fly_line.objects.get(id = sg_id)
    return render(request, 'show_detail.html', {
        "line": sgline
    })

def user_page(request, username):
    query = request.GET.get('search-keyword') 

    if query:        
        uploaded = fly_line.objects.filter(
            Q(uploader__username=username) &
            Q(removed=False) &
            (
                Q(gene_name__icontains=query) |
                Q(effector_type__icontains=query) |
                Q(source_id__icontains=query) |
                Q(cassette__icontains=query) |
                Q(contributor__icontains=query)|
                Q(citation__icontains=query)
            )
        ).order_by("status", "-date_created")
    else: 
        uploaded = fly_line.objects.filter(
            uploader__username=username
        ).order_by("status", "-date_created")

    return render(request, 'show_user.html', {
        "line_list": uploaded,
        "requested_user": username,
        "keyword": query,
    })

def update_line(request, sg_id):
    sgline = fly_line.objects.get(id = sg_id)
    form = NewLineForm(instance = sgline)

    if 'Cancel' in request.POST:
        return redirect('/show_detail/SG' + sg_id)

    if 'Update' in request.POST:
        form = NewLineForm(request.POST, instance = sgline)
        if form.is_valid():
            gene = form.cleaned_data['gene_name']
            effector = form.cleaned_data['effector_type']
            form.save()
            messages.success(
                request,(
                    f'Your edits on {gene}-{effector} are saved successfully.'
                )
            )
            return redirect('/show_detail/SG' + sg_id)
        else:
            messages.error(request,(form.errors))
            form = NewLineForm(instance=sgline)
    

    return render(request, 'update_line.html', {
        "line": sgline,
        "form": form
    })

def remove_line(request, sg_id):
    sgline = fly_line.objects.get(id = sg_id)
    form = RemoveLineForm(instance=sgline, initial={'removed': True})

    if 'Delete' in request.POST:
        form = RemoveLineForm(request.POST, instance=sgline)
        form.save()
        messages.success(request,  (
            f"You deleted {sgline.gene_name}-{sgline.effector_type}."
        )
        )
        return redirect('home')
        
    if 'Cancel' in request.POST:
        return redirect('/show_detail/SG' + sg_id)
    
    return render(request, 'remove_line.html', {
        'line': sgline,
        'form': form,
    })
    
def readme(request):
    return render(request, 'readme.html')

def privacy(request):
    return render(request, 'privacy.html')