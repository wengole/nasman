from pathlib import Path

import chardet
from django.contrib.postgres.fields import HStoreField

__author__ = 'ben'


class PathField(HStoreField):
    #TODO: Turn this into a model method to convert stored unicode to/from a
    #Path object

    description = 'A path on a filesystem.'

    def to_python(self, value):
        if isinstance(value, Path):
            return value

        if value is None:
            return value

        path = value['path'].encode(value['encoding'])
        return Path(path.decode('utf-8', 'surrogateescape'))

    def get_prep_value(self, value):
        if value is None:
            return value

        b = bytes(value)
        enc = chardet.detect(b)['encoding']
        return {'path': b.decode(enc),
                'encoding': enc}

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value

        path = value['path'].encode(value['encoding'])
        return Path(path.decode('utf-8', 'surrogateescape'))

    def validate(self, value, model_instance):
        b = bytes(value)
        enc = chardet.detect(b)['encoding']
        to_validate = {
            'path': b.decode(enc),
            'encoding': enc
        }
        return super(PathField, self).validate(to_validate, model_instance)
