from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UploadFileForm
from splitgal4_lines.models import fly_line
import openpyxl
from django.contrib.auth.decorators import login_required, user_passes_test

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

            if entry[1] == "GAL4DBD":
                effector_type = "DBD"
                activator_type = ""
            else:
                effector_type = "AD"
                activator_type = entry[1]

            if entry[1] == "Unknown AD":
                activator_type = "AD"

            cassette_dict = {
                "5' splicing acceptor": "SA",
                "N-terminus KI": "N-term",
                "C-terminus KI": "C-term",
            }

            dimerizer_dict = {
                "zip": "zip",
                "intein": "int"
            }

            status_dict = {
                "Available (Validated)": "val",
                "Available (Not validated)": "ava",
                "In progress": "inp",
                "Planned": "req",
            }

            fly_line(
                gene_name=entry[0],
                effector_type=effector_type,
                activator_type=activator_type,
                source_id=entry[2],
                ins_seqname='chr' + entry[3],
                ins_site=entry[4],
                cassette=cassette_dict[entry[5]],
                dimerizer=dimerizer_dict[entry[6]],
                status=status_dict[entry[7]],
                internal_sharing=entry[8] == 'Private',
                reference=entry[9],
                uploader=request.user.username,
                contributor=request.user.lab,
                need_review=True
            ).save()

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if "upload" in request.POST:
            # Preview first for user confirmation
            if form.is_valid():
                f = request.FILES["file"]
                request.session['payload'] = handle_uploaded_file(f)
                messages.success(request, ('File is uploaded.'))
                return render(request, "preview.html", {
                    'line_list': request.session['payload'],
                })
        elif "confirm" in request.POST:
            # If user confirms
            add_to_model(request.session['payload'])
            messages.success(request, ('Your lines are recorded.'))
            del request.session['payload']
            return redirect('home')
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})

def handle_uploaded_file(f):
    wb = openpyxl.load_workbook(f)
    worksheet = wb["List of lines"]
    excel_data = list()
    header=True
    # iterating over the rows and
    # getting value from each cell in row
    for row in worksheet.iter_rows():
        if header:
            header = False
            continue

        row_data = list()
        for cell in row:
            row_data.append(str(cell.value))
        excel_data.append(row_data)
        
    return excel_data