from django.urls import path
from employeeapi import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

router=DefaultRouter()

router.register("projectdetail",views.ProjectDetailView,basename="projectdetail")
router.register("assignedprojects",views.AssignedProjectsView,basename="assignedprojects-list")
router.register("taskchart",views.TaskChartView,basename="taskchart")
router.register("taskupdateschart",views.TaskUpdatesView,basename="taskupdateschart")
router.register("mymeeting",views.MyMeetingsView,basename="mymeeting")
router.register("technology",views.TechnologiesView,basename="tech")
router.register("myrating",views.MyRatingView,basename="rating")
router.register("dailytask",views.DailyTaskView,basename="dailytask")




urlpatterns = [
    path("register/",views.EmployeeCreateView.as_view(),name="signup"),
    path('token/',views.CustomAuthToken.as_view(), name='token'),
    path("teamview/",views.TeamView.as_view(),name="teamview"),
    path("profile/",views.profileView.as_view(),name="profile"),


    
    
] +router.urls