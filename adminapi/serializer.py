from rest_framework import serializers
from hrapi.models import Hr,Teams,TeamLead,TaskUpdateChart,TaskChart,Employee,Projects,ProjectDetail,Project_assign,Performance_assign,ProjectUpdates,Meeting



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
        fields=["description","member"]
        

class MeetingListSerializer(serializers.ModelSerializer):
    member=serializers.CharField(read_only=True)
    class Meta:
        model=Meeting
        fields="__all__"