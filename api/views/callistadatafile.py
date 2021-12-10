from rest_framework import viewsets, permissions
from api.serializers import *


class CallistaDataFileViewSet(viewsets.ModelViewSet):
    queryset = CallistaDataFile.objects.all()
    serializer_class = CallistaDataFileSerializer
    permission_classes = [permissions.IsAuthenticated]
