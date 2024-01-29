from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache

# For SSE (Server Sent Events)
from django.http import HttpResponseBadRequest
from django.http.response import StreamingHttpResponse
import asyncio


# These apps are stored separately in the DjangoDash folder.
from DjangoDash.displayData import app
from DjangoDash.loadingbardash import appBar
from django.views.generic.edit import FormView

# Forms for importing data
from .forms import CSVFile, CSVFilesForm, ExperimentForm
from .models import Experiment
import shutil
import os

from datetime import datetime

from .data_processing import process_data

# Create your views here.

from django.db import IntegrityError

# Synchronous view for handling the file upload form
def home_view(request):
    experiments = Experiment.objects.all()
    upload_progress = 0
    if request.method == 'POST':
        form = ExperimentForm(request.POST)
        csv_form = CSVFilesForm(request.POST, request.FILES)
        if form.is_valid() and csv_form.is_valid():
            cache.set('upload_progress', 'STARTED')
            experiment = form.save()
            csv_files = csv_form.cleaned_data['file']
            total_files = len(csv_files)

            # Process each file asynchronously
            for i, csv_file in enumerate(csv_files):
                # Update the upload progress
                CSVFile.objects.create(experiment=experiment, file=csv_file)
                upload_progress = (i + 1) / total_files * 100
                cache.set('upload_progress', upload_progress)
                print(upload_progress)

            # Reset the upload progress
            upload_progress = "None"
            cache.set('upload_progress', upload_progress)

            messages.success(request, 'Experiment created successfully')
            return redirect('home_view')
        else:
            cache.set('upload_progress', 'FAILED')
            messages.error(request, 'Form is not valid')

    else:
        form = ExperimentForm()
        csv_form = CSVFilesForm()

    return render(request, 'importExperiment.html', {'form': form, 'experiments': experiments, 'csv_form': csv_form})

# Asynchronous generator for SSE (upload)
async def upload_progress_stream():
    while True:
        upload_progress = cache.get('upload_progress')
        yield f"data: {upload_progress}\n\n"
        await asyncio.sleep(.5)  # Adjust as needed

# Asynchronous generator for SSE (process)
async def process_progress_stream():
    while True:
        process_progress = cache.get('process_progress')
        yield f"data: {process_progress}\n\n"
        await asyncio.sleep(.5)  # Adjust as needed

# View for SSE stream (upload progress)
def upload_sse_view(request):
    async def event_stream():
        async for data in upload_progress_stream():
            yield data
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

# View for SSE stream (process progress)
def process_sse_view(request):
    async def event_stream():
        async for data in process_progress_stream():
            yield data
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

# 

def delete_experiment(request, experiment_id):
    experiment = Experiment.objects.get(id=experiment_id)
    experiment_folder = os.path.join('media/datasets/csv_files/', experiment.name)
    numpy_file = os.path.join('media/datasets/numpy_files/', experiment.name + '.npz')  # Path to the numpy file
    shutil.rmtree(experiment_folder)  # Delete the experiment folder and all its contents

    if os.path.exists(numpy_file):  # Check if the numpy file exists
        os.remove(numpy_file)  # Delete the numpy file

    experiment.delete()
    messages.warning(request, 'Entry Deleted')
    return redirect('home_view')

def process_data_view(request):
    experiments = Experiment.objects.all()
    return render(request, 'displayProcessedData.html', {'experiments': experiments})

def process_data_button(request, experiment_id):
    if request.method == 'POST':
        cache.set('process_progress', 'STARTED')
        experiment = Experiment.objects.get(id=experiment_id)
        gas_blank_start = int(request.POST.get('gas_blank_start'))
        gas_blank_end = int(request.POST.get('gas_blank_end'))
        number_of_pixels = request.POST.get('number_of_pixels')

        # Set the attributes on the experiment instance
        experiment.gasBlankStart = gas_blank_start
        experiment.gasBlankEnd = gas_blank_end
        experiment.numberOfPixels = number_of_pixels

        # Check if number_of_pixels is an integer
        try:
            number_of_pixels = int(number_of_pixels)
        except ValueError:
            return HttpResponseBadRequest("Number of pixels must be an integer")

        # Get the selected radio button value
        calibration_type = request.POST.get('type')

        # Initialize the calibration parameters
        slope = intercept = np_size = signal_median = 0
        use_cal_curve = False

        if calibration_type == 'calCurve':
            # The Calibration Curve method was selected
            slope = float(request.POST.get('slope'))
            intercept = float(request.POST.get('intercept'))
            use_cal_curve = True

            # Set the attributes on the experiment instance
            experiment.slope = slope
            experiment.intercept = intercept
            experiment.calCurve = True

        elif calibration_type == 'singlePoint':
            # The Single Point Calibration method was selected
            np_size = float(request.POST.get('np_size'))
            signal_median = float(request.POST.get('signal_median'))
            experiment.npSize = np_size
            experiment.signalMedian = signal_median

        # Get checkbox value
        convert_to_cps = request.POST.get('convert_to_counts') is not None
        experiment.convertedToCounts = convert_to_cps

        experiment_folder = os.path.join('datasets/csv_files/', experiment.name)
        numpy_file = os.path.join('datasets/numpy_files/', experiment.name + '.npz')
        if not os.path.exists(numpy_file):
            # If the numpy file doesn't exist, process the data
            process_data(
                    experiment, 
                    experiment_folder, 
                    numpy_file,
                    convert_to_cps=convert_to_cps,
                    gas_blank_start=gas_blank_start,
                    gas_blank_end=gas_blank_end,
                    number_of_pixels=number_of_pixels,
                    cal_curve=use_cal_curve,
                    slope=slope,
                    intercept=intercept,
                    np_size=np_size,
                    signal_median=signal_median)

            # Update the processed attribute
            experiment.processed = True
            experiment.numpy_file = numpy_file

            # Save the experiment
            experiment.save()

            # Reset the process progress
            cache.set('process_progress', "None")
        
    else:
        cache.set('process_progress', 'FAILED')
            
    return redirect('process_data_view')
    
        
def display_experiment(request, experiment_id):

    if request.method == 'POST':
        experiment = Experiment.objects.get(id=experiment_id)
        numpy_file = experiment.numpy_file.path # Get the path from the model

        if os.path.exists(numpy_file):  # Check if the numpy file exists
            print('File found.')
            # Set the numpy file path in the Django session
            cache.set('numpy_file', numpy_file)
            return render(request, 'displayImages.html', {'experiment': experiment})
        else:
            print('File not found.')
            messages.warning(request, 'File not found')
            return redirect('home_view')

