from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.reverse import reverse


class UserSerializer(serializers.Serializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'date_joined')
        read_only_fields = ('username', 'date_joined')

    def get_links(self, obj):
        return {}
