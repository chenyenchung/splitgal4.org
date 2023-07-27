from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UploadFileForm
from splitgal4_lines.models import fly_line
import openpyxl
from django.contrib.auth.decorators import login_required, user_passes_test

EXAMPLE_NOTE = "This is an example. Please remove it before you upload."
TEMPLATE_CNAMES = [
    'Gene name', 'Effectors', 'MiMIC/CRIMIC #', 'chromosome',
    'location', 'cassette style', 'dimerization domain', 'status',
    'private', 'citation', 'Note'
]
DIMERIZER_DICT = {
    "zip": "zip",
    "intein": "int"
}

STATUS_DICT = {
    "Available": "1ava",
    "In progress": "2inp",
    "Planned": "3req",
}

def create_new_line(request):
    return redirect('home')

def verification_test(user):
    return user.verified

@login_required(login_url="/members/user_login")
@user_passes_test(verification_test, login_url="/members/user_login")
def upload_file(request):
    def add_to_model(data):
        for entry in data:
            entry = [i if i is not None else "" for i in entry]

            if entry[10] == EXAMPLE_NOTE:
                continue
            
            try:
                entry[4] = int(entry[4])
            except ValueError:
                entry[4] = None

            fly_line(
                gene_name=entry[0],
                effector_type=entry[1],
                source_id=entry[2],
                ins_seqname='chr' + entry[3],
                ins_site=entry[4],
                cassette=entry[5],
                dimerizer=DIMERIZER_DICT[entry[6]],
                status=STATUS_DICT[entry[7]],
                internal_sharing=entry[8] == 'Private',
                reference=entry[9],
                uploader=request.user.username,
                contributor=request.user.lab,
                contact=request.user.email,
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
    status_err = []
    dimer_err = []
    wb = openpyxl.load_workbook(f)
    if wb.__contains__('List of lines'):
        worksheet = wb["List of lines"]
        excel_data = list()
        header=True
        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            if header:
                for cname in row:
                    if cname.value not in TEMPLATE_CNAMES:
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
            if row_data[10] == EXAMPLE_NOTE:
                continue
            if row_data[7] not in STATUS_DICT:
                status_err.append(row_data[7])
            if row_data[6] not in DIMERIZER_DICT:
                dimer_err.append(row_data[6])
            excel_data.append(row_data)

        if status_err or dimer_err:
            err_show = (
                'The values in the status column must be: ' + ', '.join([str(i) for i in STATUS_DICT.keys()]),
                'The values in the dimerizer column must be: ' + ', '.join([str(i) for i in DIMERIZER_DICT.keys()])
            )

            if status_err:
                messages.error(
                    request,
                        ('Error: Unknown status found: ' + ', '.join(status_err) + '.' + err_show[0])
                )
            if dimer_err:
                messages.error(
                    request,
                        ('Error: Unknown dimerization domain found: ' + ', '.join(dimer_err) + '.' + err_show[1])
                )
            return 1
            
        return excel_data
    else:
        messages.error(
            request,
            ('The format of the template appears wrong. The website looks for sheet "List of lines"')
        )
        return 1