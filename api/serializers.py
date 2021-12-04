from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import Faculty, Unit, Course, Core, CuratedElective, Student, Enrolment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = "__all__"


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Core
        fields = "__all__"


class CuratedElectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuratedElective
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class EnrolmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrolment
        fields = "__all__"
