from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'messages', views.NotificationViewSet, base_name='messages')

urlpatterns = router.urls
