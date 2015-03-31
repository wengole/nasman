from datetime import datetime
import magic
import mock
import os

import pytz

from django.test import TestCase
from django.test.utils import override_settings
from django.utils.timezone import get_default_timezone_name

from ..models import File
from ..tasks import create_file_object


class TestCeleryTasks(TestCase):

    def setUp(self):
        cwd = os.getcwd()
        self.file_path = os.path.join(cwd, 'test-file.txt')
        f = open(self.file_path, 'w')
        f.write('Here is some text')
        f.close()
        self.statinfo = os.stat(self.file_path)
        mtime = datetime.fromtimestamp(self.statinfo.st_mtime)
        self.mtime = pytz.timezone(get_default_timezone_name()).localize(mtime)

    def tearDown(self):
        os.remove(self.file_path)

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_create_file_object(self):
        create_file_object.delay(self.file_path).get()
        file_obj = File.objects.get(
            full_path=self.file_path
        )
        self.assertIsNone(file_obj.snapshot)
        self.assertFalse(file_obj.directory)
        self.assertEqual(file_obj.modified, self.mtime)
        self.assertTrue(file_obj.size > 0)

    @override_settings(CELERY_ALWAYS_EAGER=True)
    @mock.patch('snapshots.tasks.magic.from_file')
    def test_create_file_with_magic_exception(self, mock_from_file):
        mock_from_file.side_effect = magic.MagicException
        create_file_object.delay(self.file_path).get()
        file_obj = File.objects.get(
            full_path=self.file_path
        )
        self.assertEqual(file_obj.magic, '')
        self.assertEqual(file_obj.mime_type, None)
