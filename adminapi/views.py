from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework import status
from rest_framework.decorators import action

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


from hrapi.models import *
from adminapi.serializer import *

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_type = user.user_type
        
        return Response({
            'token': token.key,
            'user_type': user_type,
        })   


class HrView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    
    def list(self,request,*args,**kwargs):
        qs=Hr.objects.filter(is_adminapproved=False)
        serializer=HrSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Hr.objects.get(id=id)
        serializer=HrSerializer(qs)
        return Response(data=serializer.data)
    
    @action(detail=True, methods=["post"])
    def approve(self, request, *args, **kwargs):
        hr_id = kwargs.get("pk")
        hr_obj = Hr.objects.get(id=hr_id)
        hr_obj.is_adminapproved = True
        hr_obj.save()
        serializer = HrSerializer(hr_obj)
        return Response(serializer.data)
        
    

class TeamleadView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    
    def list(self,request,*args,**kwargs):
        qs=TeamLead.objects.filter(is_adminapproved=False)
        serializer=TeamleadSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=TeamLead.objects.get(id=id)
        serializer=TeamleadSerializer(qs)
        return Response(data=serializer.data) 
    

    @action(detail=True, methods=["post"])
    def approve(self, request, *args, **kwargs):
        teamlead_id = kwargs.get("pk")
        teamlead_obj = TeamLead.objects.get(id=teamlead_id)
        teamlead_obj.is_adminapproved = True
        teamlead_obj.save()
        serializer = TeamleadSerializer(teamlead_obj)
        return Response(serializer.data)  
    
    

class EmployeesView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    
    def list(self,request,*args,**kwargs):
        qs=Employee.objects.filter(is_adminapproved=False)
        serializer=EmployeeSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employee.objects.get(id=id)
        serializer=EmployeeSerializer(qs)
        return Response(data=serializer.data)
    

    @action(detail=True, methods=["post"])
    def approve(self, request, *args, **kwargs):
        emp_id = kwargs.get("pk")
        emp_obj = Employee.objects.get(id=emp_id)
        emp_obj.is_adminapproved = True
        emp_obj.save()
        serializer = EmployeeSerializer(emp_obj)
        return Response(serializer.data)
    
    

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
        


class TechnologiesView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def create(self,request,*args,**kwargs):
        serializer=TechnologiesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self,request,*args,**kwargs):
        qs=TechnologiesList.objects.all()
        serializer=TechnologiesSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=TechnologiesList.objects.get(id=id)
        serializer=TechnologiesSerializer(qs)
        return Response(data=serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            instance =TechnologiesList.objects.get(id=id)
            instance.delete()
            return Response({"msg": "TechnologiesList removed"})
        except Employee.DoesNotExist:
            return Response({"msg": "TechnologiesList not found"}, status=status.HTTP_404_NOT_FOUND)
        


              