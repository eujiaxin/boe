from django.forms.forms import Form
from django.shortcuts import render
from django.urls.base import reverse, reverse_lazy
from django.views.generic.edit import FormView
from api.models import CallistaDataFile
from checkerapp.forms import CallistaDataFileMultipleUploadForm
from django.http import HttpResponse
from api.models import CallistaDataFile

# Create your views here.

# FIXME: make sure max 100 files upload -- override form validation
# TODO: already uploaded files to django. redirect to list of CSVs (checkbox page showing CSV processed or not processed yet) - need to process PUT request to handle csvs. this is where fabian comes in? (input = checked CSVs)


class CallistaDataFileCreateView(FormView):
    form_class = CallistaDataFileMultipleUploadForm
    template_name = 'checkerapp_upload_form.html'

    def get_success_url(self) -> str:
        return reverse('checkerapp:success')

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


def success(request):
    return HttpResponse('<h1>Success!</h2>')


# def processer(request):
#     if request.method == "POST":
#         files_to_delete = []
#         for key, value in request.POST.items():
#             if value == '1':
#                 files_to_delete.append(key)
#         print(files_to_delete)

#         for result_file in ResultFile.objects.all():
#             if result_file.file_name in files_to_delete:
#                 print(f"Deleting {result_file.file_name} ...")
#                 result_file.delete()

#         for graph in Graph.objects.all():
#             if graph.file_name in files_to_delete:
#                 print(f"Deleting {graph.file_name} ...")
#                 graph.delete()

#     contexts = {
#         'page_title': 'My Results',
#         'visualiser_files': [
#             f for f in ResultFile.objects.all().order_by('date_added')
#         ],
#     }
#     return render(request, "plotter/mygraphs.html", context=contexts)
