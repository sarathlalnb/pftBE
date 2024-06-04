from django.urls import path
from teamleadapi import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

router=DefaultRouter()

router.register("team",views.TeamView,basename="team-create")
router.register("employee",views.EmployeesView,basename="employee")
router.register("projects",views.ProjectView,basename="projects-list")
router.register("assignedprojects",views.AssignedProjectView,basename="assignedprojects-list")
router.register("projectdetail",views.ProjectDetailView,basename="projectdetail")
router.register("taskchart",views.TaskChartView,basename="taskchart")
router.register("meeting",views.MeetingView,basename="meeting")
router.register("dailytask",views.DailyTaskView,basename="dailytask")
router.register("performance",views.PerformancelistView,basename="performance")






urlpatterns = [
    path("register/",views.TeamleadCreateView.as_view(),name="signup"),
    path('token/',views.CustomAuthToken.as_view(), name='token'),
    path("profile/",views.profileView.as_view(),name="profile"),


]  +router.urls