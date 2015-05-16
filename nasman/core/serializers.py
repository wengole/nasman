from rest_framework import serializers

from .models import Notification
from nasman.snapshots.models import ZFSFilesystem, ZFSSnapshot


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('message', 'created', )


class ZFSFilesystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZFSFilesystem
        fields = ('name', 'mountpoint', )


class ZFSSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZFSSnapshot
        fields = ('name', 'timestamp', )
