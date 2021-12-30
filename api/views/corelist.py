from rest_framework import viewsets, permissions
from api.serializers import *


class CoreListViewSet(viewsets.ModelViewSet):
    queryset = CoreList.objects.all()
    serializer_class = CoreListSerializer
    permission_classes = [permissions.IsAuthenticated]
