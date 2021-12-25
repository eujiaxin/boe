from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.edit import FormView
from api.models import CallistaDataFile, Student
from checkerapp.forms import CallistaDataFileMultipleUploadForm
from api.models import CallistaDataFile
import scripts.process_csv as pc

user_to_output = dict()


class CallistaDataFileCreateView(FormView):
    form_class = CallistaDataFileMultipleUploadForm
    template_name = 'checkerapp_upload_form.html'

    def get_success_url(self) -> str:
        return reverse('checkerapp:processor')

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


def processor(request):
    global user_to_output
    if request.method == "POST":
        files_posted = []
        for key, value in request.POST.items():
            if value == '1':
                files_posted.append(int(key))
        print("files_posted: ", files_posted)
        student_set = set()
        for file in CallistaDataFile.objects.filter(pk__in=files_posted):
            student_set.update(pc.bulk_pc(file))
            file.has_been_processed = True
            file.save()
        user_to_output[request.user.username] = list(student_set)
        return HttpResponseRedirect(reverse('checkerapp:validator'))
    context = {
        'callista_files': [
            f for f in CallistaDataFile.objects.all().order_by('upload_date')
        ],
    }
    return render(request, "checkerapp_process_form.html", context=context)


def validator(request):
    if request.method == "POST":
        if request.user.username in user_to_output:
            output = dict()
            for student in user_to_output[request.user.username]:
                output[student] = student.validate_graduation()
            return render(request, "checkerapp_success_page.html", {'output': output})
        return HttpResponse("No student request...")
    context = {
        "students": user_to_output[request.user.username]
    }
    return render(request, "checkerapp_validate_form.html", context=context)
