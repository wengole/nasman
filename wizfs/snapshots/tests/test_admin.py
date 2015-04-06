from django.contrib import admin
from django.test import TestCase


class TestModelAdmins(TestCase):

    def setUp(self):
        self.admin_site = admin.site

    def test_admins_are_registered(self):
        registered = [str(x) for x in self.admin_site._registry.values()]
        self.assertIn('snapshots.SnapshotAdmin', registered)
        self.assertIn('snapshots.FileAdmin', registered)
