from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from snapshots.models import File
from snapshots.forms import FileForm
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django.http import Http404


class FileListView(ListView):
    model = File
    template_name = "snapshots/file_list.html"
    paginate_by = 20
    context_object_name = "file_list"
    allow_empty = True
    page_kwarg = 'page'
    paginate_orphans = 0

    def __init__(self, **kwargs):
        return super(FileListView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(FileListView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(FileListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return super(FileListView, self).get_queryset()

    def get_allow_empty(self):
        return super(FileListView, self).get_allow_empty()

    def get_context_data(self, *args, **kwargs):
        ret = super(FileListView, self).get_context_data(*args, **kwargs)
        return ret

    def get_paginate_by(self, queryset):
        return super(FileListView, self).get_paginate_by(queryset)

    def get_context_object_name(self, object_list):
        return super(FileListView, self).get_context_object_name(object_list)

    def paginate_queryset(self, queryset, page_size):
        return super(FileListView, self).paginate_queryset(queryset, page_size)

    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True):
        return super(FileListView, self).get_paginator(queryset, per_page, orphans=0, allow_empty_first_page=True)

    def render_to_response(self, context, **response_kwargs):
        return super(FileListView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(FileListView, self).get_template_names()


class FileDetailView(DetailView):
    model = File
    template_name = "snapshots/file_detail.html"
    context_object_name = "file"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'

    def __init__(self, **kwargs):
        return super(FileDetailView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(FileDetailView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(FileDetailView, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(FileDetailView, self).get_object(queryset)

    def get_queryset(self):
        return super(FileDetailView, self).get_queryset()

    def get_slug_field(self):
        return super(FileDetailView, self).get_slug_field()

    def get_context_data(self, **kwargs):
        ret = super(FileDetailView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(FileDetailView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(FileDetailView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(FileDetailView, self).get_template_names()


class FileCreateView(CreateView):
    model = File
    form_class = FileForm
    fields = ['full_path', 'snapshot', 'mime_type', 'extension', 'created', 'modified', 'size']
    template_name = "snapshots/file_create.html"
    success_url = reverse_lazy("file_list")

    def __init__(self, **kwargs):
        return super(FileCreateView, self).__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        return super(FileCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(FileCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(FileCreateView, self).post(request, *args, **kwargs)

    def get_form_class(self):
        return super(FileCreateView, self).get_form_class()

    def get_form(self, form_class):
        return super(FileCreateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(FileCreateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(FileCreateView, self).get_initial()

    def form_invalid(self, form):
        return super(FileCreateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(FileCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(FileCreateView, self).get_context_data(**kwargs)
        return ret

    def render_to_response(self, context, **response_kwargs):
        return super(FileCreateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(FileCreateView, self).get_template_names()

    def get_success_url(self):
        return reverse("file_detail", args=(self.object.pk,))


class FileUpdateView(UpdateView):
    model = File
    form_class = FileForm
    fields = ['full_path', 'snapshot', 'mime_type', 'extension', 'created', 'modified', 'size']
    template_name = "snapshots/file_update.html"
    initial = {}
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = "file"

    def __init__(self, **kwargs):
        return super(FileUpdateView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(FileUpdateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(FileUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(FileUpdateView, self).post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(FileUpdateView, self).get_object(queryset)

    def get_queryset(self):
        return super(FileUpdateView, self).get_queryset()

    def get_slug_field(self):
        return super(FileUpdateView, self).get_slug_field()

    def get_form_class(self):
        return super(FileUpdateView, self).get_form_class()

    def get_form(self, form_class):
        return super(FileUpdateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(FileUpdateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(FileUpdateView, self).get_initial()

    def form_invalid(self, form):
        return super(FileUpdateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(FileUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(FileUpdateView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(FileUpdateView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(FileUpdateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(FileUpdateView, self).get_template_names()

    def get_success_url(self):
        return reverse("file_detail", args=(self.object.pk,))


class FileDeleteView(DeleteView):
    model = File
    template_name = "snapshots/file_delete.html"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = "file"

    def __init__(self, **kwargs):
        return super(FileDeleteView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(FileDeleteView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        return super(FileDeleteView, self).post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super(FileDeleteView, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(FileDeleteView, self).get_object(queryset)

    def get_queryset(self):
        return super(FileDeleteView, self).get_queryset()

    def get_slug_field(self):
        return super(FileDeleteView, self).get_slug_field()

    def get_context_data(self, **kwargs):
        ret = super(FileDeleteView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(FileDeleteView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(FileDeleteView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(FileDeleteView, self).get_template_names()

    def get_success_url(self):
        return reverse("file_list")
