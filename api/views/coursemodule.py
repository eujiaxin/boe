from rest_framework import generics, viewsets, permissions
from api.serializers import *


class CourseModuleViewSet(viewsets.ModelViewSet):
    queryset = CourseModule.objects.all()
    serializer_class = CourseModuleSerializer
    permission_classes = [permissions.IsAuthenticated]
