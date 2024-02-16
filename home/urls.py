from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.home_view, name='home_view'),
    path('delete_experiment/<int:experiment_id>/', views.delete_experiment, name='delete_experiment'),
    path('process_data/',views.process_data_view, name='process_data_view'),
    path('process_data_button/<int:experiment_id>/', views.process_data_button, name='process_data_button'),
    path('display_experiment/<int:experiment_id>/', views.display_experiment, name='display_experiment'),
    path('process_sse_view/', views.process_sse_view, name='process_sse_view'),
    path('upload_sse_view/', views.upload_sse_view, name='upload_sse_view'),
    path('download_csv/<int:experiment_id>/', views.download_csv, name='download_csv'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)