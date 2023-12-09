"""
from rest_framework import serializers
from .models import *

# class CalenderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Calendar
#         fields = '__all__'

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'

"""