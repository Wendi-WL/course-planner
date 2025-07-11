from rest_framework import serializers
from scraper.models import Course 

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__' # Include all fields from the Course model