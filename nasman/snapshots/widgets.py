import logging
import floppyforms as forms

logger = logging.getLogger(__name__)

class BootstrapClassesMixin(object):
    """
    Mixin for adding classes to form widgets
    """
    def get_context_data(self):
        classes = getattr(self, 'classes', ['form-control'])
        context = super().get_context_data()
        context.update({
            'classes': classes
        })
        return context


class SmallSelectWidget(BootstrapClassesMixin, forms.Select):
    classes = ['input-sm', 'form-control']


class BootstrapCheckboxWidget(BootstrapClassesMixin, forms.CheckboxInput):
    classes = ['checkbox']


class BootstrapTextWidget(BootstrapClassesMixin, forms.TextInput):
    pass


class BootstrapSelectWidget(BootstrapClassesMixin, forms.Select):
    pass
