from rest_framework import generics, viewsets, permissions
from api.serializers import *


class EnrolmentViewSet(viewsets.ModelViewSet):
    queryset = Enrolment.objects.all()
    serializer_class = EnrolmentSerializer
    permission_classes = [permissions.IsAuthenticated]
