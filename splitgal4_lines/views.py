from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from .models import fly_line
from .forms import NewLineForm

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
            ).order_by("status")
        else:
            line_list = fly_line.objects.filter(
                (Q(internal_sharing=see_all) |
                Q(internal_sharing=False) |
                Q(contributor=request.user.lab)|
                Q(uploader=request.user.username))
            ).order_by("status")
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

def add_line(request):
    try:
        prefill_contr = request.user.lab
    except:
        prefill_contr = 'Anonymous user'

    try:
        prefill_email = request.user.email
    except:
        prefill_email = ''

    if request.user.username == '':
        prefill_uploader = 'Anonymous user'
    else:
        prefill_uploader = request.user.username

    if request.method == "POST":
      form = NewLineForm(request.POST)
      if form.is_valid():   
          gene = request.POST["gene_name"]
          form.save()
          messages.success(
              request, (f'Your line for {gene} is uploaded successfully.')
          )
          return redirect('home')
    else:
      form = NewLineForm(
          initial = {
              'contributor': prefill_contr,
              'uploader': prefill_uploader,
              'contact': prefill_email
          }
      )

    return render(request, 'idv_upload.html', {
         'form': form,
      })

def readme(request):
    return(render(request, 'readme.html'))