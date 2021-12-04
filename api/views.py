from django.contrib.auth.models import User, Group
from rest_framework import generics, viewsets, permissions
from api.serializers import *


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class FacultyListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FacultySerializer
    queryset = Faculty.objects.all()


class FacultyRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FacultySerializer
    queryset = Faculty.objects.all()


class UnitListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UnitSerializer
    queryset = Unit.objects.all()


class UnitRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UnitSerializer
    queryset = Unit.objects.all()


class CourseListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class CourseListByCodeAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseSerializer
    lookup_fields = ['course_code']
    queryset = Course.objects.all()


class CourseRetrieveByCodeAndVersionAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseSerializer
    lookup_fields = ['course_code', 'course_version']
    queryset = Course.objects.all()


class CourseRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class CoreListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CoreSerializer
    queryset = Core.objects.all()


class CoreRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CoreSerializer
    queryset = Core.objects.all()


class CuratedElectiveListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CuratedElectiveSerializer
    queryset = CuratedElective.objects.all()


class CuratedElectiveRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CuratedElectiveSerializer
    queryset = CuratedElective.objects.all()


class StudentListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()


class StudentRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()


class EnrolmentListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EnrolmentSerializer
    queryset = Enrolment.objects.all()


class EnrolmentRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EnrolmentSerializer
    queryset = Enrolment.objects.all()
