from django.shortcuts import render
from rest_framework import authentication, filters, mixins, permissions, viewsets

from core.views import DefaultsMixin
from .models import HelpRequest, HelpRequestReply
from .serializers import HelpRequestSerializer, HelpRequestReplySerializer


class HelpRequestViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = HelpRequest.objects.all().not_closed().only_future_meetings()
    serializer_class = HelpRequestSerializer

    def get_queryset(self):
        queryset = self.queryset
        user_latitude = self.request.query_params.get('user_latitude', None)
        user_longitude = self.request.query_params.get('user_longitude', None)
        radius = self.request.query_params.get('radius', None)

        if user_latitude is not None and user_longitude is not None:
            if radius is not None:
                queryset = queryset.location(user_latitude, user_longitude,
                                             radius)
            else:
                queryset = queryset.location(user_latitude, user_longitude)

        return queryset


class HelpRequestReplyViewSet(DefaultsMixin,
                              mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.DestroyModelMixin,
                              mixins.UpdateModelMixin,
                              viewsets.GenericViewSet):
    queryset = HelpRequestReply.objects.all()
    serializer_class = HelpRequestReplySerializer
