from django.db import models


class Snapshot(models.Model):
    """
    Model representing s ZFS snapshot
    """
    name = models.CharField('name', max_length=255)
    timestamp = models.DateTimeField('timestamp', null=True, blank=True)

    class Meta:
        unique_together = ()
        index_together = ()

    def __unicode__(self):
        return self.name


class File(models.Model):
    """
    Model representing a file/directory/etc on the filesystem
    """
    full_path = models.CharField('full path', max_length=255)
    snapshot = models.ForeignKey(
        Snapshot,
        verbose_name='snapshot',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    mime_type = models.CharField('mime type', blank=True, max_length=255)
    extension = models.CharField('extension', blank=True, max_length=255)
    created = models.DateTimeField('created')
    modified = models.DateTimeField('modified')
    size = models.IntegerField('size', blank=True, null=True)

    class Meta:
        unique_together = ()
        index_together = ()

    def __unicode__(self):
        return self.full_path