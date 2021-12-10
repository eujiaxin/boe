from django import forms


class CallistaDataFileMultipleUploadForm(forms.Form):
    name = forms.CharField(max_length=50)
    uploads = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
