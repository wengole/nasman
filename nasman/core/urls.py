from rest_framework.routers import DefaultRouter

from . import views

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

urlpatterns = router.urls
