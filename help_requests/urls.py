from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from help_requests import views

router = DefaultRouter()
router.register(r'help-requests', views.HelpRequestViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls))
]
