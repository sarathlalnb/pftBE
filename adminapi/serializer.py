from rest_framework import serializers
from hrapi.models import *



class HrSerializer(serializers.ModelSerializer):
    class Meta:
        model=Hr
        fields=["id","name","email_address","phoneno","user_type","is_adminapproved"]

class TeamleadSerializer(serializers.ModelSerializer):
    class Meta:
        model=TeamLead
        fields=["id","name","email_address","phoneno","user_type","is_adminapproved"]

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        fields=["id","Firstname","lastname","email_address","phoneno","position","user_type","in_team","is_adminapproved"]
        

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Meeting
        fields=["title","link","date","time"]
        

class MeetingListSerializer(serializers.ModelSerializer):
    organizer=serializers.CharField(read_only=True)
    class Meta:
        model=Meeting
        fields="__all__"
        

class TechnologiesSerializer(serializers.ModelSerializer):
    class Meta:
        model=TechnologiesList
        fields="__all__"