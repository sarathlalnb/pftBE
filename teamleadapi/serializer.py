from rest_framework import serializers
from hrapi.models import *

class RegistrationSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=TeamLead
        fields=["id","name","email_address","phoneno","home_address","job_title","position","department","prefferred_timezone","linkedin_profile","skills","certification","experience","username","password"]

    def create(self, validated_data):
        return TeamLead.objects.create_user(**validated_data)


class ProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model=TeamLead
        fields=["id","name","email_address","phoneno","home_address","job_title","position","department","prefferred_timezone","linkedin_profile","skills","certification","experience"]

        
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Projects
        fields="__all__"
        
        
class ProjectAssignSerializer(serializers.ModelSerializer):
    project=serializers.CharField(read_only=True)
    teamlead=serializers.CharField(read_only=True)
    team=serializers.CharField(read_only=True)
    class Meta:
        model=Project_assign
        fields="__all__"
        
class ProjectDetailSerializer(serializers.ModelSerializer):
    projectassigned=serializers.CharField(read_only=True)
    teamlead=serializers.CharField(read_only=True)
    class Meta:
        model=ProjectDetail
        fields="__all__"
        
class ProjectDetailViewSerializer(serializers.ModelSerializer):
    projectassigned=serializers.CharField(read_only=True)
    teamlead=serializers.CharField(read_only=True)
    assigned_person=serializers.CharField(source='assigned_person.name', read_only=True)
    class Meta:
        model=ProjectDetail
        fields="__all__"
        
        
class TeamSerializer(serializers.ModelSerializer):
    teamlead=serializers.CharField(read_only=True)
    class Meta:
        model=Teams
        fields="__all__"
        
class TeamsViewSerializer(serializers.ModelSerializer):
    teamlead=serializers.CharField(read_only=True)
    members=serializers.SerializerMethodField()

    def get_members(self, obj):
        return [member.employee.name for member in obj.members.all()]
    
    class Meta:
        model=Teams
        fields="__all__"
        
        
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        fields=["id","name","email_address","phoneno","home_address","job_title","department","linkedin_profile","manager_name","resume","start_date","user_type","in_team"]
        
        
class TaskChartSerializer(serializers.ModelSerializer):
    project_detail=ProjectDetailSerializer()
    assigned_person=serializers.CharField(source='assigned_person.name', read_only=True)
    project_name=serializers.CharField(source='project_detail.projectassigned.project', read_only=True)  #new field for project name
    class Meta:
        model=TaskChart
        fields="__all__"
        

class TaskUpdatesChartSerializer(serializers.ModelSerializer):
    class Meta:
        model=TaskUpdateChart
        fields="__all__"


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Meeting
        fields=["title","link","date","time"]
        

class MeetingListSerializer(serializers.ModelSerializer):
    member=serializers.CharField(read_only=True)
    class Meta:
        model=Meeting
        fields="__all__"  
        
        
class DailyTaskSerializer(serializers.ModelSerializer):
    teamlead=serializers.CharField(read_only=True)
    emp=serializers.CharField(read_only=True)
    class Meta:
        model=DailyTask
        fields="__all__"
        

class RatingSerializer(serializers.ModelSerializer):
    teamlead=serializers.CharField(read_only=True)
    emp=serializers.CharField(read_only=True)
    class Meta:
        model=Rating
        fields="__all__" 

        
        
class PerformanceSerializer(serializers.ModelSerializer):
    teamlead=serializers.CharField(read_only=True)

    class Meta:
        model=Performance_assign
        fields="__all__" 
        
        
class PerformanceListSerializer(serializers.ModelSerializer):
    teamlead=serializers.CharField(read_only=True)
    employee=serializers.CharField(read_only=True)
    
    class Meta:
        model=Performance_assign
        fields="__all__"