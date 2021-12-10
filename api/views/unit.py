from rest_framework import viewsets, permissions
from api.serializers import *


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]
