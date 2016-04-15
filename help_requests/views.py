from django.shortcuts import render
from rest_framework import authentication, filters, mixins, permissions, viewsets
from rest_framework.response import Response

from core.views import DefaultsMixin
from .models import HelpRequest, HelpRequestReply
from .serializers import HelpRequestSerializer, HelpRequestReplySerializer


class HelpRequestViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = HelpRequest.objects.all().not_closed().only_future_meetings()
    serializer_class = HelpRequestSerializer

    def list(self, request):
        queryset = HelpRequest.objects.all().not_closed().only_future_meetings()

        user_latitude = request.query_params.get('user_latitude', None)
        user_longitude = request.query_params.get('user_longitude', None)
        radius = request.query_params.get('radius', None)

        if user_latitude is not None and user_longitude is not None:
            if radius is not None:
                queryset = queryset.location(user_latitude, user_longitude,
                                             radius)
            else:
                queryset = queryset.location(user_latitude, user_longitude)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class HelpRequestReplyViewSet(DefaultsMixin,
                              mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.DestroyModelMixin,
                              mixins.UpdateModelMixin,
                              viewsets.GenericViewSet):
    queryset = HelpRequestReply.objects.all()
    serializer_class = HelpRequestReplySerializer
