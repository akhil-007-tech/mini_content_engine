from django.urls import path
from .views import home, GenerateAPIView, JobStatusAPIView

urlpatterns = [
    path("", home, name="home"),
    path("generate/", GenerateAPIView.as_view(), name="generate"),
    path("status/<uuid:job_id>/", JobStatusAPIView.as_view(), name="status"),
]