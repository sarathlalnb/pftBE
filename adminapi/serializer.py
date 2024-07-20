from rest_framework import serializers
from hrapi.models import *



class HrSerializer(serializers.ModelSerializer):
    class Meta:
        model=Hr
        fields=["id","name","email_address","phoneno","home_address","job_title","position","department","prefferred_timezone","linkedin_profile","skills","certification","experience","is_adminapproved"]
        

class TeamleadSerializer(serializers.ModelSerializer):
    class Meta:
        model=TeamLead
        fields=["id","name","email_address","phoneno","home_address","job_title","position","department","prefferred_timezone","linkedin_profile","skills","certification","experience"]
    
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        fields=["id","name","email_address","phoneno","home_address","job_title","department","linkedin_profile","manager_name","resume","start_date","in_team"]        
       

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