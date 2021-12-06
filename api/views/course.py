from rest_framework import generics, viewsets, permissions
from api.serializers import *
from api.views.custom import *


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]


# class CourseRetrieveByCodeAndVersionAPIView(MultipleFieldLookupMixin, generics.RetrieveAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = CourseSerializer
#     queryset = Course.objects.all()
#     lookup_fields = ['course_code', 'course_version']
