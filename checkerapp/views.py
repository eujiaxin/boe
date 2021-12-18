from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.edit import FormView
from api.models import CallistaDataFile
from checkerapp.forms import CallistaDataFileMultipleUploadForm
from django.http import HttpResponse
from api.models import CallistaDataFile
import scripts.process_csv as pc
from scripts.process_reqs import validate_graduation

# Create your views here.

# FIXME: make sure max 100 files upload -- override form validation
# TODO: already uploaded files to django. redirect to list of CSVs (checkbox page showing CSV processed or not processed yet) - need to process PUT request to handle csvs. this is where fabian comes in? (input = checked CSVs)


class CallistaDataFileCreateView(FormView):
    form_class = CallistaDataFileMultipleUploadForm
    template_name = 'checkerapp_upload_form.html'

    def get_success_url(self) -> str:
        return reverse('checkerapp:processer')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('uploads')
        if form.is_valid():
            for csv in files:
                print(form.cleaned_data)
                # add each CSV as an callista object
                obj = CallistaDataFile.objects.create(
                    name=form.cleaned_data['name'],
                    upload=csv
                )
                print(obj)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def success(_):
    return HttpResponse('<h1>Success!</h2>')


def processer(request):
    if request.method == "POST":
        files_posted = []
        for key, value in request.POST.items():
            if value == '1':
                files_posted.append(int(key))
        print("files_posted: ", files_posted)
        student_set = {}
        for file in CallistaDataFile.objects.filter(pk__in=files_posted):
            student_set.union(pc.bulk_pc(file))
        output = validate_graduation(list(student_set))

    contexts = {
        'callista_files': [
            f for f in CallistaDataFile.objects.all().order_by('upload_date')
        ],
    }
    return render(request, "checkerapp_process_form.html", context=contexts)
