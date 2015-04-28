from django.db import models
from django.utils.translation import ugettext as _

from .icon import Icon
from .forms import IconFormField


class IconField(models.Field):
    description = _('A fontawesome icon field')
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 60
        kwargs['blank'] = True
        super(IconField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    def to_python(self, value):
        if value is None or value == 'None':
            return None

        if isinstance(value, Icon):
            return value

        # default => string
        return Icon(icon_id=value)

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def get_prep_value(self, value):
        return str(value)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': IconFormField,
            # 'choices_form_class':IconFormField
        }

        defaults.update(kwargs)
        return super(IconField, self).formfield(**defaults)
