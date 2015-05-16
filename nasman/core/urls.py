from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'notifications', views.NotificationViewSet, base_name='notifications')

urlpatterns = router.urls
