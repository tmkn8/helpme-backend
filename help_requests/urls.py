from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from accounts import views as acc_views
from help_requests import views as hr_views

router = DefaultRouter()
router.register(r'help-requests', hr_views.HelpRequestViewSet)
router.register(r'users', acc_views.UserViewSet)
router.register(r'help-request-reply', hr_views.HelpRequestReplyViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls))
]
