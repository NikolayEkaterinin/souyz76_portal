from django.urls import path, include

from .views import UploadExcelView
app_name = 'params'

urlpatterns = [
    path('load_objects/', UploadExcelView.as_view(), name='load_objects'),

]
