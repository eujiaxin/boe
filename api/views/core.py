from rest_framework import viewsets, permissions
from api.serializers import *


class CoreViewSet(viewsets.ModelViewSet):
    queryset = Core.objects.all()
    serializer_class = CoreSerializer
    permission_classes = [permissions.IsAuthenticated]
