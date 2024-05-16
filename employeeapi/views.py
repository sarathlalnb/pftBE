from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework import status
from rest_framework.decorators import action
from datetime import datetime, timedelta
from rest_framework.exceptions import PermissionDenied,NotFound



from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


from hrapi.models import *
from employeeapi.serializer import *


class EmployeeCreateView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="employee")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_obj=Employee.objects.get(id=user.id)
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

        
        
class TeamView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        try:
            employee = Employee.objects.get(id=request.user.id)
        except Employee.DoesNotExist:
            return Response({"error": "Employee does not exist"}, status=status.HTTP_404_NOT_FOUND)
        qs = Teams.objects.filter(members=employee).distinct()
        serializer = TeamSerializer(qs, many=True)
        return Response(serializer.data)
    

class AssignedProjectsView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        try:
            employee = Employee.objects.get(id=request.user.id)
        except Employee.DoesNotExist:
            return Response({"error": "Employee does not exist"}, status=status.HTTP_404_NOT_FOUND)
        emp_id=request.user.id
        qs = Project_assign.objects.filter(team__members=employee).distinct()
        serializer = ProjectAssignSerializer(qs, many=True)
        
        for project_assign_data in serializer.data:
            project_assign = Project_assign.objects.get(id=project_assign_data['id'])
            project_details = ProjectDetail.objects.filter(projectassigned=project_assign,assigned_person=emp_id)
            project_detail_serializer = ProjectDetailSerializer(project_details, many=True)
            project_detail_data = project_detail_serializer.data
            
            project_assign_data['project_details'] = project_detail_data
        
        return Response(serializer.data)
    
    # def retrieve(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     qs=Project_assign.objects.get(id=id)
    #     serializer=ProjectAssignSerializer(qs)
    #     return Response(data=serializer.data)
    

    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        project_id=Projects.objects.get(id=id)
        
        try:
            project_assign = Project_assign.objects.get(id=id)
        except Project_assign.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        project_assign_serializer = ProjectAssignSerializer(project_assign)
        project_assign_data = project_assign_serializer.data
        project_details = ProjectDetail.objects.filter(projectassigned=project_assign)
        project_detail_serializer = ProjectDetailSerializer(project_details, many=True)
        project_detail_data = project_detail_serializer.data
        project_assign_data['project_details'] = project_detail_data
        project_updates = ProjectUpdates.objects.filter(project=project_id)
        project_updates_serializer = ProjectUpdatesSerializer(project_updates, many=True)
        project_updates_data = project_updates_serializer.data
        project_assign_data['project_updates'] = project_updates_data
        
        return Response(data=project_assign_data)
     
    
    
class ProjectDetailView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        emp_id=request.user.id
        qs=ProjectDetail.objects.filter(assigned_person=emp_id)
        serializer=ProjectDetailSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        emp_id=request.user.id
        qs=ProjectDetail.objects.get(id=id,assigned_person=emp_id)
        serializer=ProjectDetailSerializer(qs)
        return Response(data=serializer.data)
    
    
    @action(methods=["post"], detail=True)
    def taskchart_add(self, request, *args, **kwargs):
        serializer = TaskChartSerializer(data=request.data)
        projectdetail_id = kwargs.get("pk")
        projectdetail_obj = ProjectDetail.objects.get(id=projectdetail_id)
        emp_id = request.user.id
        emp_obj = Employee.objects.get(id=emp_id)       
        if projectdetail_obj.assigned_person != emp_obj:
            raise PermissionDenied("You are not authorized to create task charts for this project detail.")
        if serializer.is_valid():
            start_date = datetime.now().date()
            ending_date = projectdetail_obj.projectassigned.project.end_date
            total_days = (ending_date - start_date).days if ending_date else None
            serializer.save(assigned_person=emp_obj, project_detail=projectdetail_obj, total_days=total_days, end_date=ending_date)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    @action(methods=["post"],detail=True)
    def part_complete(self, request, *args, **kwargs):
        projectdetail = kwargs.get("pk")
        try:
            projectdetail_obj = ProjectDetail.objects.get(id=projectdetail)
        except Project_assign.DoesNotExist:
            return Response({"message": "project not found"}, status=status.HTTP_404_NOT_FOUND)
        projectdetail_obj.status = "completed"
        projectdetail_obj.save()
        return Response({"message": "project part completed marked success"}, status=status.HTTP_200_OK)
        

class TaskChartView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        try:
            employee = Employee.objects.get(id=request.user.id)
        except Employee.DoesNotExist:
            return Response({"error": "Employee does not exist"}, status=status.HTTP_404_NOT_FOUND)
        qs = TaskChart.objects.filter(assigned_person=employee)
        serializer = TaskChartSerializer(qs, many=True)
        return Response(serializer.data)
    
    
    # def retrieve(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     emp_id=request.user.id
    #     qs=TaskChart.objects.get(id=id,assigned_person=emp_id)
    #     serializer=TaskChartSerializer(qs)
    #     return Response(data=serializer.data)
    
    
    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        emp_id = request.user.id
        try:
            task_chart = TaskChart.objects.get(id=id, assigned_person=emp_id)
        except TaskChart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        task_chart_serializer = TaskChartSerializer(task_chart)
        task_chart_data = task_chart_serializer.data
        task_updates = TaskUpdateChart.objects.filter(task=task_chart)
        task_updates_serializer = TaskUpdateChartSerializer(task_updates, many=True)
        task_updates_data = task_updates_serializer.data
        task_chart_data['task_updates'] = task_updates_data
        return Response(data=task_chart_data)
    
    
    @action(methods=["post"],detail=True)
    def taskupdates_add(self, request, *args, **kwargs):
        serializer=TaskUpdateChartSerializer(data=request.data)
        task_id=kwargs.get("pk")
        task_obj=TaskChart.objects.get(id=task_id)
        emp_id=request.user.id
        emp_obj=Employee.objects.get(id=emp_id)       
        if serializer.is_valid():
            serializer.save(updated_by=emp_obj,task=task_obj)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    
class TaskUpdatesView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        emp_id=request.user.id
        qs=TaskUpdateChart.objects.filter(updated_by=emp_id)
        serializer=TaskUpdateChartSerializer(qs,many=True)
        return Response(data=serializer.data)   
    
    
class MyMeetingsView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    
    def list(self,request,*args,**kwargs):
        qs=Meeting.objects.all()
        serializer=MeetingListSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Meeting.objects.get(id=id)
        serializer=MeetingListSerializer(qs)
        return Response(data=serializer.data)
    
    
class profileView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self,request,*args,**kwargs):
        emp_id=request.user.id
        qs=Employee.objects.get(id=emp_id)
        serializer=RegistrationSerializer(qs)
        return Response(serializer.data)
    
    
    def put(self, request, *args, **kwargs): 
        emp_id = request.user.id
        try:
            emp = Employee.objects.get(id=emp_id)
        except Employee.DoesNotExist:
            return Response({"error": "Employee does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileEditSerializer(instance=emp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

class TechnologiesView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    
    def list(self,request,*args,**kwargs):
        qs=TechnologiesList.objects.all()
        serializer=TechnologiesSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=TechnologiesList.objects.get(id=id)
        serializer=TechnologiesSerializer(qs)
        return Response(data=serializer.data)
        


class MyRatingView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        emp_id=request.user.id
        qs=Rating.objects.filter(emp=emp_id)
        serializer=RatingSerializer(qs,many=True)
        return Response(serializer.data)  
    
    
class DailyTaskView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        emp_id=request.user.id
        emp_obj=Employee.objects.get(id=emp_id)
        qs=DailyTask.objects.filter(emp=emp_obj,is_completed=False)
        serializer=DailyTaskSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=DailyTask.objects.get(id=id)
        serializer=DailyTaskSerializer(qs)
        return Response(data=serializer.data)  
    
    @action(detail=True, methods=["post"])
    def mark_completed(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        qs=DailyTask.objects.get(id=id)
        qs.is_completed= True
        qs.save()
        serializer = DailyTaskSerializer(qs)
        return Response(serializer.data)     