from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import HelpRequest, HelpRequestReply


class HelpRequestReplySerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = HelpRequestReply
        fields = '__all__'
        read_only_fields = ('author', 'help_request', 'id')

    def get_author_name(self, obj):
        return obj.help_request.author_name


class HelpRequestSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()
    help_request_replies = HelpRequestReplySerializer(many=True, read_only=True)

    class Meta:
        model = HelpRequest
        fields = ['id', 'title', 'author_name', 'datetime', 'location_name', 'meeting_datetime',
                  'location_lat', 'location_lon', 'content', 'is_closed', 'help_request_replies', 'links']
        read_only_fields = ('author', 'datetime')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('helprequest-detail', kwargs={'pk': obj.pk},
                            request=request),
            'author': None,
        }

    def save(self, *args, **kwargs):
        super(HelpRequestSerializer, self).save(*args, author=self.context['request'].user, **kwargs)
