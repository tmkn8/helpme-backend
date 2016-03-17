from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect

from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.reverse import reverse
from rest_framework.response import Response

from core.views import DefaultsMixin
from .serializers import UserSerializer, UserPrivateSerializer


class UserViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    @list_route(methods=['get', 'put'])
    def me(self, request):
        self.serializer_class = UserPrivateSerializer

        user = request.user

        if not user.is_authenticated():
            raise PermissionDenied

        serializer = UserPrivateSerializer(user,
                                           context={'request': request})

        if request.method == 'PUT':
            serializer = UserPrivateSerializer(user,
                                               data=request.data,
                                               context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)
