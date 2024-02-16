from django.db import models
import os

# Create your models here.

def experiment_csv_upload_path(instance, filename):
    # instance is the CSVFile object, and filename is the original CSV file name
    # Create a folder with the experiment name and keep the original file name
    upload_path = os.path.join('datasets/csv_files/', instance.experiment.name)
    os.makedirs(upload_path, exist_ok=True)
    return os.path.join(upload_path, filename)

class Experiment(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    processed = models.BooleanField(default=False) # True if the experiment has been processed
    numpy_file = models.FileField(upload_to='datasets/numpy_files/')
    # These fields are for the data processing
    gasBlankStart = models.IntegerField(default=0)
    gasBlankEnd = models.IntegerField(default=0)
    numberOfPixels = models.IntegerField(default=20)
    calCurve = models.BooleanField(default=False)
    npSize = models.FloatField(default=0)
    signalMedian = models.FloatField(default=0)
    slope = models.FloatField(default=0)
    intercept = models.FloatField(default=0)
    corrupted = models.BooleanField(default=False)
    convertedToCounts = models.BooleanField(default=False)

class CSVFile(models.Model):
    file = models.FileField(upload_to=experiment_csv_upload_path)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, default=None, null=True, blank=True)