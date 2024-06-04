from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Count, Sum, F, ExpressionWrapper, FloatField

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


from hrapi.models import Hr,Teams,TeamLead,TaskUpdateChart,TaskChart,Employee,Projects,ProjectDetail,Project_assign,Performance_assign,ProjectUpdates,Meeting
# from hrapi.serializer import RegistrationSerializer,EmployeeSerializer,TeamleadSerializer,TeamsSerializer,ProjectSerializer,ProjectAssignSerializer,ProjectDetailSerializer,TaskChartSerializer,TaskUpdatesChartSerializer,PerformanceTrackSerializer,PerformanceTrackViewSerializer,ProjectUpdatesSerializer
from hrapi.serializer import *

class HrCreateView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="hr")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_obj=Hr.objects.get(id=user.id)
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
        qs=Employee.objects.all()
        serializer=EmployeeSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employee.objects.get(id=id)
        serializer=EmployeeSerializer(qs)
        return Response(data=serializer.data)
    

class TeamleadView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    
    def list(self,request,*args,**kwargs):
        qs=TeamLead.objects.all()
        serializer=TeamleadSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=TeamLead.objects.get(id=id)
        serializer=TeamleadSerializer(qs)
        return Response(data=serializer.data)
    

class TeamsView(ViewSet):    
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    # def create(self,request,*args,**kwargs):
    #     serializer=TeamsSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)

    
    def list(self,request,*args,**kwargs):
        qs=Teams.objects.all()
        serializer=TeamsSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Teams.objects.get(id=id)
        serializer=TeamsSerializer(qs)
        return Response(data=serializer.data)
    
    
    @action(detail=True, methods=["post"])
    def team_approval(self, request, *args, **kwargs):
        team_id = kwargs.get("pk")
        team_obj = Teams.objects.get(id=team_id)
        team_obj.is_approved = True
        team_obj.save()
        serializer = TeamsSerializer(team_obj)
        return Response(serializer.data)
    
    
class ProjectView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def create(self,request,*args,**kwargs):
        serializer=ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self,request,*args,**kwargs):
        qs=Projects.objects.all()
        serializer=ProjectSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Projects.objects.get(id=id)
        serializer=ProjectSerializer(qs)
        return Response(data=serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            instance =Projects.objects.get(id=id)
            instance.delete()
            return Response({"msg": "Projects removed"})
        except Employee.DoesNotExist:
            return Response({"msg": "Projects not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
    @action(detail=True, methods=["post"])
    def create_updates(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Projects.objects.get(id=id)
        serializer=ProjectUpdatesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=qs)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 


class ProjectUpdatesView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
       
       
    def list(self,request,*args,**kwargs):
        qs=ProjectUpdates.objects.all()
        serializer=ProjectUpdatesSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=ProjectUpdates.objects.get(id=id)
        serializer=ProjectUpdatesSerializer(qs)
        return Response(data=serializer.data)
 


class ProjectAssignView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=Project_assign.objects.all()
        serializer=ProjectAssignSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Project_assign.objects.get(id=id)
        serializer=ProjectAssignSerializer(qs)
        return Response(data=serializer.data)
      
        
    
class ProjectDetailView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=ProjectDetail.objects.all()
        serializer=ProjectDetailSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=ProjectDetail.objects.get(id=id)
        serializer=ProjectDetailSerializer(qs)
        return Response(data=serializer.data)
    

class TaskChartView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=TaskChart.objects.all()
        serializer=TaskChartSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    
    
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
    
    
class PerformanceTrackView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = PerformanceTrackSerializer(data=request.data)
        hr_id = request.user.id
        hr_obj = Hr.objects.get(id=hr_id)
        employee_id = request.data.get('employee')  
        employee = Employee.objects.get(id=employee_id)
        
        task_count = TaskUpdateChart.objects.filter(updated_by=employee).count()
        
        total_days_spent = TaskUpdateChart.objects.filter(updated_by=employee).aggregate(
            total_days_spent=Sum('task__total_days')
        )['total_days_spent'] or 0
        
        total_days_assigned = TaskChart.objects.filter(assigned_person=employee).aggregate(
            total_days_assigned=Sum('total_days')
        )['total_days_assigned'] or 0
        
        if total_days_assigned > 0:
            tasks_percentage = min((task_count / total_days_assigned) * 100, 100)
        else:
            tasks_percentage = 0
        
        if total_days_assigned > 0:
            days_percentage = min((total_days_spent / total_days_assigned) * 100, 100)  
        else:
            days_percentage = 0
        
        overall_performance = min((tasks_percentage + days_percentage) / 2, 100)
        
        if serializer.is_valid():
            serializer.save(
                hr=hr_obj,
                employee=employee,
                performance=overall_performance
            )
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
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
        hr_id=request.user.id
        qs=Hr.objects.get(id=hr_id)
        serializer=RegistrationSerializer(qs)
        return Response(serializer.data)
    
    def put(self, request, *args, **kwargs): 
        hr_id = request.user.id
        try:
            hr = Hr.objects.get(id=hr_id)
        except Hr.DoesNotExist:
            return Response({"error": "hr does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileEditSerializer(instance=hr, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ReviewView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=Rating.objects.all()
        serializer=ReviewSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Rating.objects.get(id=id)
        serializer=ReviewSerializer(qs)
        return Response(data=serializer.data)