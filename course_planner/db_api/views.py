from django.shortcuts import render
from rest_framework import viewsets
from scraper.models import Course
from .serializers import CourseSerializer

# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    """
    queryset = Course.objects.all() # The set of objects the viewset will operate on
    serializer_class = CourseSerializer # The serializer to use for this viewset