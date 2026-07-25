from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import render
from .models import Job
from .serializers import JobSerializer
from .tasks import process_job



def home(request):
    return render(request, "index.html")

class GenerateAPIView(generics.CreateAPIView):
    """
    Create a new image generation job.
    """
    
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            job = serializer.save()

            # Send job to Celery
            process_job(str(job.id))

            return Response(
                {
                    "message": "Job created successfully",
                    "job_id": str(job.id),
                    "status": job.status,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class JobStatusAPIView(APIView):
    """
    Check job status.
    """

    def get(self, request, job_id):

        try:
            job = Job.objects.get(id=job_id)

        except Job.DoesNotExist:
            return Response(
                {"error": "Job not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = JobSerializer(job)

        return Response(serializer.data)