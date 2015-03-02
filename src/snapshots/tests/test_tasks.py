from datetime import datetime
import os

import pytz

from django.test import TestCase
from django.test.utils import override_settings
from django.utils.timezone import get_default_timezone_name

from ..models import File
from ..tasks import create_file_object


class TestCeleryTasks(TestCase):

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_create_file_object(self):
        cwd = os.getcwd()
        file_path = os.path.join(cwd, 'test-file.txt')
        f = open(file_path, 'w')
        f.write('Here is some text')
        f.close()
        statinfo = os.stat(file_path)
        mtime = datetime.fromtimestamp(statinfo.st_mtime)
        mtime = pytz.timezone(get_default_timezone_name()).localize(mtime)
        create_file_object.delay(file_path).get()

        file_obj = File.objects.get(
            full_path=file_path
        )
        self.assertIsNone(file_obj.snapshot)
        self.assertFalse(file_obj.directory)
        self.assertEqual(file_obj.modified, mtime)
        self.assertTrue(file_obj.size > 0)
