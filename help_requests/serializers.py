from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import HelpRequest


class HelpRequestSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = HelpRequest
        fields = ['id', 'title', 'author_name', 'datetime', 'location_name',
                  'location_lat', 'location_lon', 'content', 'is_closed', 'links']
        read_only_fields = ('author', 'datetime')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('helprequest-detail', kwargs={'pk': obj.pk},
                            request=request),
            'author': None,
        }
