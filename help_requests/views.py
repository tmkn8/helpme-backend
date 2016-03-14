from django.shortcuts import render
from rest_framework import authentication, filters, permissions, viewsets

from .models import HelpRequest
from .serializers import HelpRequestSerializer


class HelpRequestViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = HelpRequest.objects.all()
    serializer_class = HelpRequestSerializer

    def get_queryset(self):
        queryset = self.queryset
        user_latitude = self.request.query_params.get('user_latitude', None)
        user_longitude = self.request.query_params.get('user_longitude', None)
        radius = self.request.query_params.get('radius', None)
        print(user_longitude)
        print(user_latitude)
        if user_latitude is not None and user_longitude is not None:
            if radius is not None:
                queryset = queryset.location(user_latitude, user_longitude,
                                             radius)
            else:
                queryset = queryset.location(user_latitude, user_longitude)

        return queryset
