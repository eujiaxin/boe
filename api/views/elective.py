from rest_framework import viewsets, permissions
from api.serializers import *


class ElectiveViewSet(viewsets.ModelViewSet):
    queryset = Elective.objects.all()
    serializer_class = ElectiveSerializer
    permission_classes = [permissions.IsAuthenticated]
