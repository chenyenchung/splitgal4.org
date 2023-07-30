from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
import openpyxl

from .forms import UploadFileForm, NewLineForm, AnonNewLineForm
from splitgal4_lines.models import fly_line



EXAMPLE_NOTE = settings.EXAMPLE_NOTE
TEMPLATE = settings.TEMPLATE
TEMPLATE_CNAMES = TEMPLATE.field_labels

def verification_test(user):
    return user.verified

@login_required(login_url="/members/user_login")
@user_passes_test(verification_test, login_url="/members/user_login")
def upload_file(request):
    def add_to_model(data):
        for entry in data:
            entry = [i if i is not None else "" for i in entry]

            # The note field is always the last and not defined in
            # the instruction
            note_col = TEMPLATE.get_field_index('notes')

            if entry[note_col] == EXAMPLE_NOTE:
                continue
            
            
            try:
                entry[TEMPLATE.get_field_index('ins_site')] = int(entry[TEMPLATE.get_field_index('ins_site')])
            except ValueError:
                entry[TEMPLATE.get_field_index('ins_site')] = None

            # If the user provided alternative contributor, use it.
            # Otherwise the host lab is the contributor.
            if entry[TEMPLATE.get_field_index('contributor')] != '':
                contributor = entry[TEMPLATE.get_field_index('contributor')]
                contact = ''
            else:
                contributor = request.user.lab
                contact = request.user.email

            fly_line(
                gene_name=entry[TEMPLATE.get_field_index('gene_name')],
                effector_type=entry[TEMPLATE.get_field_index('effector_type')],
                source_id=entry[TEMPLATE.get_field_index('source_id')],
                ins_seqname='chr' + entry[TEMPLATE.get_field_index('ins_seqname')],
                ins_site=entry[TEMPLATE.get_field_index('ins_site')],
                cassette=entry[TEMPLATE.get_field_index('cassette')],
                dimerizer=entry[TEMPLATE.get_field_index('dimerizer')],
                status=entry[TEMPLATE.get_field_index('status')],
                private=entry[TEMPLATE.get_field_index('private')] == "Private",
                citation=entry[TEMPLATE.get_field_index('citation')],
                notes=entry[TEMPLATE.get_field_index('notes')],
                uploader=request.user,
                contributor=contributor,
                contact=contact,
                need_review=True
            ).save()

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if "upload" in request.POST:
            # Preview first for user confirmation
            if form.is_valid():
                f = request.FILES["file"]
                request.session['payload'] = handle_uploaded_file(f, request)
                if request.session['payload'] != 1:
                    messages.success(request, ('File is uploaded.'))
                    return render(request, "preview.html", {
                        'line_list': request.session['payload'],
                    })
                else:
                    render(request, "upload.html", {"form": form})
        elif "confirm" in request.POST:
            # If user confirms
            add_to_model(request.session['payload'])
            messages.success(request, ('Your lines are recorded.'))
            del request.session['payload']
            return redirect('home')
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})

def handle_uploaded_file(f, request):
    wb = openpyxl.load_workbook(f)
    if wb.__contains__('List of lines'):
        worksheet = wb["List of lines"]
        
        # Prepare to record illegal field values
        err_dict = dict()
        for defined_field in TEMPLATE.field_opts.keys():
            err_dict[defined_field] = []
        
        excel_data = list()
        header=True
        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            error_found = False
            if header:
                for ncol, cname in enumerate(row):
                    if cname.value not in TEMPLATE_CNAMES and ncol < len(row) - 1:
                        messages.error(
                            request,
                            (cname.value + ' is not a legit column name in the\
                            template. Please do not change column names and orders.')
                        )
                        return 1
                header = False
                continue

            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            
            # Examine data integrity

            # Skip examples
            note_col = TEMPLATE.get_field_index('notes')
            if row_data[note_col] == EXAMPLE_NOTE:
                continue

            for defined_field in TEMPLATE.field_opts.keys():
                legit_choices = TEMPLATE.field_choices[defined_field]
                this_cell = row_data[TEMPLATE.get_field_index(defined_field)]
    
                if this_cell not in legit_choices and this_cell != "None":
                    if this_cell not in err_dict[defined_field]:
                        err_dict[defined_field].append(this_cell)
                        error_found = True

            if error_found:
                continue


            # Replace None with ''
            row_data = ['' if i == 'None' else i for i in row_data]
            excel_data.append(row_data)

        error_found = [len(err_dict[err_key]) for err_key in err_dict]
        if max(error_found) > 0:
            for err_key in err_dict:
                if len(err_dict[err_key]) == 0:
                    continue
                
                err_i = ', '.join(err_dict[err_key])
                legit_choices = TEMPLATE.field_choices[err_key]
                report = 'Error: Unknown ' + err_key + ' found: ' + err_i + '. '
                legit_disclaimer = 'The values in the ' + err_key + ' column must be: ' + ', '.join(legit_choices)
                messages.error(
                    request,
                    (report + legit_disclaimer)
                )
            return 1
            
        return excel_data
    else:
        messages.error(
            request,
            ('The format of the template appears wrong. The website looks for sheet "List of lines"')
        )
        return 1

def add_line(request):
    init_dict = {}
    try:
        init_dict['contributor'] = request.user.lab
    except:
        init_dict['contributor'] = ''

    try:
        init_dict['contact'] = request.user.email
    except:
        init_dict['contact'] = ''

    if request.user.is_authenticated:
        init_dict['uploader'] = request.user   


    if request.method == "POST":
      if request.user.is_authenticated:
        init_dict['uploader'] = request.user
        form = NewLineForm(request.POST)
      else:
        form = AnonNewLineForm(request.POST)

      if form.is_valid():   
          gene = request.POST["gene_name"]
          form.save()
          messages.success(
              request, (f'Your line for {gene} is uploaded successfully.')
          )
          return redirect('home')

    else:
      if request.user.is_authenticated:
        init_dict['uploader'] = request.user
        form = NewLineForm(initial=init_dict)
      else:
        form = AnonNewLineForm(initial=init_dict)


    return render(request, 'idv_upload.html', {
         'form': form,
      })