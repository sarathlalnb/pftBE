from django.urls import path
from adminapi import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter


router=DefaultRouter()
router.register("hr",views.HrView,basename="hr")
router.register("teamlead",views.TeamleadView,basename="teamlead")
router.register("employee",views.EmployeesView,basename="employee")
router.register("meeting",views.MeetingView,basename="meeting")
router.register("technology",views.TechnologiesView,basename="tech")





urlpatterns = [
    
    path('token/',views.CustomAuthToken.as_view(), name='token'),
    
] +router.urls
