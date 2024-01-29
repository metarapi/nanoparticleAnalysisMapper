from django import forms
from .models import CSVFile
from .models import Experiment

class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 20, 'rows': 1}),
        }

class MultipleCSVFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleCSVFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleCSVFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class CSVFilesForm(forms.ModelForm):
    class Meta:
        model = CSVFile
        fields = ('file',)

    file = MultipleCSVFileField()  # Use the custom MultipleFileField for the csv_files field

class ProcessForm(forms.Form):
    experiment = forms.ModelChoiceField(queryset=Experiment.objects.all())
    gasBlankStart = forms.IntegerField()
    gasBlankEnd = forms.IntegerField()
    numberOfPixels = forms.IntegerField()
    calCurve = forms.BooleanField()
    npSize = forms.FloatField()
    signalMedian = forms.FloatField()
    slope = forms.FloatField()
    intercept = forms.FloatField()