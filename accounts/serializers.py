from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.reverse import reverse


class UserSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['username', 'date_joined', 'is_staff', 'links']
        read_only_fields = ['username', 'date_joined', 'is_staff']

    def get_links(self, obj):
        request = self.context['request']
        return {}


class UserPrivateSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['email', 'is_staff']
        read_only_fields = UserSerializer.Meta.read_only_fields + ['is_staff']
