from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied,NotFound

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


from hrapi.models import *
from teamleadapi.serializer import *


class TeamleadCreateView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="teamlead")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
 
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_obj=TeamLead.objects.get(id=user.id)
        user_approved=user_obj.is_adminapproved
        if user_approved:
            token, created = Token.objects.get_or_create(user=user)
            user_type = user.user_type
            return Response({
                'token': token.key,
                'user_type': user_type,
            })
        else:
            return Response(data={"msg": "You are not approved by admin"}, status=status.HTTP_403_FORBIDDEN)
 
        
    
class EmployeesView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    
    def list(self,request,*args,**kwargs):
        # qs=Employee.objects.filter(in_team=False)
        qs=Employee.objects.all()
        serializer=EmployeeSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employee.objects.get(id=id)
        serializer=EmployeeSerializer(qs)
        return Response(data=serializer.data)
    
    
    @action(detail=True, methods=["post"])
    def rate_emp(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        tl_id = request.user.id
        tl_obj = TeamLead.objects.get(id=tl_id)
        qs=Employee.objects.get(id=id)
        serializer=RatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(emp=qs,teamlead=tl_obj)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    @action(detail=True, methods=["post"])
    def add_task(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        tl_id = request.user.id
        tl_obj = TeamLead.objects.get(id=tl_id)
        qs=Employee.objects.get(id=id)
        serializer=DailyTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(emp=qs,teamlead=tl_obj)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class DailyTaskView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=DailyTask.objects.all()
        serializer=DailyTaskSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=DailyTask.objects.get(id=id)
        serializer=DailyTaskSerializer(qs)
        return Response(data=serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            instance =DailyTask.objects.get(id=id)
            instance.delete()
            return Response({"msg": "Task removed"})
        except Employee.DoesNotExist:
            return Response({"msg": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
    
    
    
    
class TeamView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = TeamSerializer(data=request.data)
        teamlead_id = request.user.id
        teamlead_obj = TeamLead.objects.get(id=teamlead_id)
        
        if serializer.is_valid():
            employee_ids = request.data.get('members', [])
            employees_already_in_team = Employee.objects.filter(id__in=employee_ids, in_team=True)
            if employees_already_in_team.exists():
                error_msg="selected employees are already part of a team and cannot be added to yours."
                return Response(data={"error": error_msg}, status=status.HTTP_400_BAD_REQUEST)
            team = serializer.save(teamlead=teamlead_obj)
            employees_added_to_team = team.members.all()
            employees_added_to_team.update(in_team=True)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    def list(self, request, *args, **kwargs):
        teamlead_id = request.user.id
        teamlead_obj = TeamLead.objects.get(id=teamlead_id)
        try:
            team = Teams.objects.get(teamlead=teamlead_obj)
        except Teams.DoesNotExist:
            return Response(data={"message": "Team not found for this team lead."}, status=status.HTTP_404_NOT_FOUND)
        serializer = TeamsViewSerializer(team)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Teams.objects.get(id=id)
        serializer=TeamsViewSerializer(qs)
        return Response(data=serializer.data)
    
    
class ProjectView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=Projects.objects.all()
        serializer=ProjectSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Projects.objects.get(id=id)
        serializer=ProjectSerializer(qs)
        return Response(data=serializer.data)
     
    @action(methods=["post"],detail=True)
    def project_assign(self,request,*args,**kwargs):
        serializer=ProjectAssignSerializer(data=request.data)
        project_id=kwargs.get("pk")
        project_obj=Projects.objects.get(id=project_id)
        teamlead=request.user.id
        teamlead_obj=TeamLead.objects.get(id=teamlead)
        team_obj=Teams.objects.get(teamlead=teamlead_obj)
        if team_obj.is_approved==True:
            if serializer.is_valid():
                project_obj.project_status="Ongoing"
                project_obj.save()
                serializer.save(project=project_obj,teamlead=teamlead_obj,team=team_obj)
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"message": "Team is not approved by the Hr, so team cannot accept projects."}, status=status.HTTP_404_NOT_FOUND)
    

class AssignedProjectView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        teamlead_id=request.user.id
        qs=Project_assign.objects.filter(teamlead=teamlead_id)
        serializer=ProjectAssignSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        assigned_project_id = kwargs.get("pk")
        
        try:
            assigned_project_obj = Project_assign.objects.get(id=assigned_project_id)
            project_detail = assigned_project_obj.project
            project_serializer = ProjectSerializer(project_detail)
            project_assign_serializer = ProjectAssignSerializer(assigned_project_obj)
            
            return Response({
                'project_detail': project_serializer.data,
                'assigned_project_detail': project_assign_serializer.data
            })
        except Project_assign.DoesNotExist:
            raise NotFound("Assigned project not found")
    
    
    @action(methods=["post"], detail=True)
    def assign_to_emp(self, request, *args, **kwargs):
        serializer = ProjectDetailSerializer(data=request.data)
        projectassign_id = kwargs.get("pk")
        projectassign_obj = Project_assign.objects.get(id=projectassign_id)
        teamlead = request.user.id
        teamlead_obj = TeamLead.objects.get(id=teamlead)
        if projectassign_obj.teamlead != teamlead_obj:
            raise PermissionDenied("You are not authorized to assign this project to employees.")
        assigned_employee_id = request.data.get('assigned_person')
        assigned_employee = Employee.objects.get(id=assigned_employee_id)
        team = projectassign_obj.team
        if assigned_employee not in team.members.all():
            raise PermissionDenied("You can only assign this project to your team members.")
        if serializer.is_valid():
            serializer.save(teamlead=teamlead_obj, projectassigned=projectassign_obj)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        
    @action(methods=["post"],detail=True)
    def project_completed(self, request, *args, **kwargs):
        assignedproject_id = kwargs.get("pk")
        try:
            assignproject_obj = Project_assign.objects.get(id=assignedproject_id)
        except Project_assign.DoesNotExist:
            return Response({"message": "project not found"}, status=status.HTTP_404_NOT_FOUND)
        assignproject_obj.project.project_status = "completed"
        assignproject_obj.project.save()
        return Response({"message": "project completed marked success"}, status=status.HTTP_200_OK)
        
        
class ProjectDetailView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        teamlead_id=request.user.id
        qs=ProjectDetail.objects.filter(teamlead=teamlead_id)
        serializer=ProjectDetailViewSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=ProjectDetail.objects.get(id=id)
        serializer=ProjectDetailViewSerializer(qs)
        return Response(data=serializer.data)
    

class TaskChartView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        teamlead_id = request.user.id
        qs = TaskChart.objects.filter(project_detail__teamlead=teamlead_id)
        serializer = TaskChartSerializer(qs, many=True)
        return Response(serializer.data)
    
    
    def retrieve(self, request, *args, **kwargs):
        try:
            task_chart = TaskChart.objects.prefetch_related('taskupdatechart_set').get(id=kwargs.get("pk"))
        except TaskChart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TaskChartSerializer(task_chart)
        data = serializer.data
        task_updates_chart_list = task_chart.taskupdatechart_set.all()
        task_updates_chart_serializer = TaskUpdatesChartSerializer(task_updates_chart_list, many=True)
        data['task_updates_chart_list'] = task_updates_chart_serializer.data
        return Response(data)
    
    
# class TaskUpdatesChartView(ViewSet):
#     authentication_classes=[authentication.TokenAuthentication]
#     permission_classes=[permissions.IsAuthenticated]
    
#     def list(self,request,*args,**kwargs):
#         qs=TaskUpdateChart.objects.all()
#         serializer=TaskUpdatesChartSerializer(qs,many=True)
#         return Response(data=serializer.data)
    
#     def retrieve(self,request,*args,**kwargs):
#         id=kwargs.get("pk")
#         qs=TaskUpdateChart.objects.get(id=id)
#         serializer=TaskUpdatesChartSerializer(qs)
#         return Response(data=serializer.data)
    
    
    
class MeetingView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def create(self,request,*args,**kwargs):
        serializer=MeetingSerializer(data=request.data)
        user_id=request.user.username
        if serializer.is_valid():
            serializer.save(organizer=user_id)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self,request,*args,**kwargs):
        qs=Meeting.objects.all()
        serializer=MeetingListSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Meeting.objects.get(id=id)
        serializer=MeetingListSerializer(qs)
        return Response(data=serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            instance =Meeting.objects.get(id=id)
            instance.delete()
            return Response({"msg": "Meeting removed"})
        except Employee.DoesNotExist:
            return Response({"msg": "Meeting not found"}, status=status.HTTP_404_NOT_FOUND)
        
          

class profileView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self,request,*args,**kwargs):
        TeamLead_id=request.user.id
        qs=TeamLead.objects.get(id=TeamLead_id)
        serializer=RegistrationSerializer(qs)
        return Response(serializer.data)
    
    def put(self, request, *args, **kwargs): 
        teamlead_id = request.user.id
        try:
            teamlead = TeamLead.objects.get(id=teamlead_id)
        except TeamLead.DoesNotExist:
            return Response({"error": "TeamLead does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileEditSerializer(instance=teamlead, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          

    
     
class PerformancelistView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=Performance_assign.objects.all()
        serializer=PerformanceTrackViewSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            instance =Performance_assign.objects.get(id=id)
            instance.delete()
            return Response({"msg": "performance removed"})
        except Employee.DoesNotExist:
            return Response({"msg": "performance not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
