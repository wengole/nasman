from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views
from nasman.core.views import DashboardView

router = DefaultRouter()
router.register(
    r'notifications',
    views.NotificationViewSet,
    base_name='notifications'
)
router.register(
    r'zfs-filesystems',
    views.ZFSFilesystemViewSet,
    base_name='zfs-filesystems'
)
router.register(
    r'zfs-snapshots',
    views.ZFSSnapshotViewSet,
    base_name='zfs-snapshots'
)

urlpatterns = (
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^$', DashboardView.as_view(), name='dashboard'),
)
