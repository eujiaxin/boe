from django.contrib.auth.models import User, Group
from rest_framework import generics, viewsets, permissions
from api.serializers import *


# Custom Mixin class
class MultipleFieldLookupMixin:
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """

    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]:  # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = generics.get_object_or_404(
            queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


class CreateUpdateAPIView(generics.CreateAPIView, generics.UpdateAPIView):
    pass


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
    lookup_field = 'unit_code'
    queryset = Unit.objects.all()


# FIXME: edit unit_code -> new instance created instead of update? (it only works for other fields)
# FIXME: How to only use UpdateAPIView?? (there's no pre-filled fields thingy)
class UnitUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UnitSerializer
    lookup_field = 'unit_code'
    queryset = Unit.objects.all()


class UnitCreateUpdateAPIView(CreateUpdateAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UnitSerializer
    queryset = Unit.objects.all()
    lookup_field = 'unit_code'

    def get_object(self):
        filter = {self.lookup_field: self.kwargs[self.lookup_field]}
        obj = generics.get_object_or_404(self.get_queryset(), **filter)
        print(obj)
        self.check_object_permissions(self.request, obj)
        return obj


class CourseListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class CourseListByCodeAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_queryset(self):
        """
        Return list of all courses filtered by the course code
        """
        return Course.objects.filter(course_code=self.kwargs['course_code'])


class CourseRetrieveByCodeAndVersionAPIView(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    lookup_fields = ['course_code', 'course_version']


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

# FIXME: can create duplicates!


class CuratedElectiveCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
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
    lookup_field = 'student_id'


class StudentCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
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


class EnrolmentCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = EnrolmentSerializer
    queryset = Enrolment.objects.all()
