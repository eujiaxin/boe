"""boe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.db.models import base
from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from api.views import *
from api.views import callistadatafile


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
router = routers.DefaultRouter()
router.register(r'faculties', faculty.FacultyViewSet, basename='faculty')
router.register(r'students', student.StudentViewSet, basename="student")
router.register(r'units', unit.UnitViewSet, basename="unit")
router.register(r'cores', core.CoreViewSet, basename="core")
router.register(r'courses', course.CourseViewSet, basename="course")
router.register(r'enrolments', enrolment.EnrolmentViewSet,
                basename="enrolment")
router.register(r'ce', curatedelective.CuratedElectiveViewSet,
                basename="curatedelective")
router.register(r'callista', callistadatafile.CallistaDataFileViewSet,
                basename="callista")
router.register(r'users', user.UserViewSet, basename="user")
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('checkerapp/', include('checkerapp.urls'))
]
