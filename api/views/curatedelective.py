from rest_framework import viewsets, permissions
from api.serializers import *


class CuratedElectiveViewSet(viewsets.ModelViewSet):
    queryset = CuratedElective.objects.all()
    serializer_class = CuratedElectiveSerializer
    permission_classes = [permissions.IsAuthenticated]
