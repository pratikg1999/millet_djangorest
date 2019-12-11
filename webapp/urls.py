from django.urls import path
from .views import *

urlpatterns = [
    path('file', FileUploadView.as_view()),
    path('employees', EmployeeList.as_view()),
]