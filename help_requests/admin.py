from django.contrib import admin

from .models import HelpRequest, HelpRequestReply


class HelpRequestReplyInline(admin.TabularInline):
    model = HelpRequestReply
    extra = 0


@admin.register(HelpRequest)
class HelpRequestAdmin(admin.ModelAdmin):
    inlines = [HelpRequestReplyInline]
