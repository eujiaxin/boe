from rest_framework import viewsets, permissions
from api.serializers import *


class WrapperViewSet(viewsets.ModelViewSet):
    queryset = Wrapper.objects.all()
    serializer_class = WrapperSerializer
    permission_classes = [permissions.IsAuthenticated]
