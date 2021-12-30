from rest_framework import generics, viewsets, permissions
from api.serializers import *


class ElectiveListViewSet(viewsets.ModelViewSet):
    queryset = ElectiveList.objects.all()
    serializer_class = ElectiveListSerializer
    permission_classes = [permissions.IsAuthenticated]
