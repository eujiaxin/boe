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
from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from api.views import *

faculty_endpoints = [
    path('', FacultyListAPIView.as_view()),
    path('<int:pk>/', FacultyRetrieveAPIView.as_view())
]

unit_endpoints = [
    path('', UnitListAPIView.as_view()),
    path('<str:unit_code>/', UnitRetrieveAPIView.as_view()),
    path('<str:unit_code>/createupdate/', UnitCreateUpdateAPIView.as_view()),
    path('<str:unit_code>/update/', UnitUpdateAPIView.as_view())
]

course_endpoints = [
    path('', CourseListAPIView.as_view()),
    path('<str:course_code>/', CourseListByCodeAPIView.as_view()),
    path(
        '<str:course_code>/<str:course_version>/',
        CourseRetrieveByCodeAndVersionAPIView.as_view()
    )
]

student_endpoints = [
    path('', StudentListAPIView.as_view()),
    path('create/', StudentCreateAPIView.as_view()),
    path('<str:student_id>/', StudentRetrieveAPIView.as_view()),

]

core_endpoints = [
    path('', CoreListAPIView.as_view()),
    path('<int:pk>/', CoreRetrieveAPIView.as_view())
]

ce_endpoints = [
    path('', CuratedElectiveListAPIView.as_view()),
    path('create/', CuratedElectiveCreateAPIView.as_view()),
    path('<int:pk>/', CuratedElectiveCreateAPIView.as_view())
]

enrolment_endpoints = [
    path('', EnrolmentListAPIView.as_view()),
    path('create/', EnrolmentCreateAPIView.as_view()),
    path('<int:pk>/', EnrolmentRetrieveAPIView.as_view()),
]

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('faculties/', include(faculty_endpoints)),
    path('units/', include(unit_endpoints)),
    path('courses/', include(course_endpoints)),
    path('students/', include(student_endpoints)),
    path('cores/', include(core_endpoints)),
    path('ce/', include(ce_endpoints)),
    path('enrolments/', include(enrolment_endpoints)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls)
]
