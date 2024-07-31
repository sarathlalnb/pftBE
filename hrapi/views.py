from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Count, Sum, F, ExpressionWrapper, FloatField
from rest_framework.views import APIView

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.db import IntegrityError


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
                 'id':user.id,
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

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get("pk")

        try:
            team_instance = Teams.objects.get(pk=pk)
            for member in team_instance.members.all():
                member.in_team = False
                member.save()
            team_instance.members.clear()
            team_instance.delete()
            return Response({"msg": "Team removed"})
        except Teams.DoesNotExist:
            return Response({"msg": "Team not found"}, status=status.HTTP_404_NOT_FOUND)
    
    
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
        
    def put(self,request,*args,**kwargs):
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
    
       
        
class PerformancelistView(ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    
    def list(self,request,*args,**kwargs):
        qs=Performance_assign.objects.all()
        serializer=PerformanceTrackViewSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def get(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        print(id)
     
        emp=Employee.objects.get(id=id)
        qs=Performance_assign.objects.get(employee=emp)
        serializer=PerformanceTrackViewSerializer(qs)
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


class PerfomanceCreateView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        try:
            user_obj = Employee.objects.get(id=pk)
            team_lead = TeamLead.objects.get(id=request.user.id)
        except Employee.DoesNotExist:
            return Response({"status": 0, "error": "employee not found"}, status=status.HTTP_404_NOT_FOUND)
       
        serializer = PerformanceTrackSerializer2(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(teamlead=team_lead, employee=user_obj)
                response_data = {
                    "status": 1,
                    "data": serializer.data
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"status": 0, "error": "performance entry for this employee already exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, pk, *args, **kwargs):
        try:
            user_obj = Employee.objects.get(id=pk)
            team_lead = TeamLead.objects.get(id=request.user.id)
        except Employee.DoesNotExist:
            return Response({"status": 0, "error": "employee not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            perf=request.data.get('performance')
            print(perf)
            p=Performance_assign.objects.get(employee=user_obj)
            p.performance=perf
            p.save()
            response_data = {
                "status": 1,
                "data": perf
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"status": 0, "error": "Some error occured!!!!"}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, pk, *args, **kwargs):
        try:
            user_obj = Employee.objects.get(id=pk)
            team_lead = TeamLead.objects.get(id=request.user.id)
        except Employee.DoesNotExist:
            return Response({"status": 0, "error": "employee not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            p=Performance_assign.objects.get(employee=user_obj)
           
            response_data = {
                "status": 1,
                "data": p.performance
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"status": 0, "error": "Some error occured!!!!"}, status=status.HTTP_400_BAD_REQUEST)
