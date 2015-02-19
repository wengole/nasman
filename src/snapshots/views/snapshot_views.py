from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from snapshots.models import Snapshot
from snapshots.forms import SnapshotForm
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django.http import Http404


class SnapshotListView(ListView):
    model = Snapshot
    template_name = "snapshots/snapshot_list.html"
    paginate_by = 20
    context_object_name = "snapshot_list"
    allow_empty = True
    page_kwarg = 'page'
    paginate_orphans = 0

    def __init__(self, **kwargs):
        return super(SnapshotListView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(SnapshotListView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(SnapshotListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return super(SnapshotListView, self).get_queryset()

    def get_allow_empty(self):
        return super(SnapshotListView, self).get_allow_empty()

    def get_context_data(self, *args, **kwargs):
        ret = super(SnapshotListView, self).get_context_data(*args, **kwargs)
        return ret

    def get_paginate_by(self, queryset):
        return super(SnapshotListView, self).get_paginate_by(queryset)

    def get_context_object_name(self, object_list):
        return super(SnapshotListView, self).get_context_object_name(object_list)

    def paginate_queryset(self, queryset, page_size):
        return super(SnapshotListView, self).paginate_queryset(queryset, page_size)

    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True):
        return super(SnapshotListView, self).get_paginator(queryset, per_page, orphans=0, allow_empty_first_page=True)

    def render_to_response(self, context, **response_kwargs):
        return super(SnapshotListView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(SnapshotListView, self).get_template_names()


class SnapshotDetailView(DetailView):
    model = Snapshot
    template_name = "snapshots/snapshot_detail.html"
    context_object_name = "snapshot"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'

    def __init__(self, **kwargs):
        return super(SnapshotDetailView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(SnapshotDetailView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(SnapshotDetailView, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(SnapshotDetailView, self).get_object(queryset)

    def get_queryset(self):
        return super(SnapshotDetailView, self).get_queryset()

    def get_slug_field(self):
        return super(SnapshotDetailView, self).get_slug_field()

    def get_context_data(self, **kwargs):
        ret = super(SnapshotDetailView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(SnapshotDetailView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(SnapshotDetailView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(SnapshotDetailView, self).get_template_names()


class SnapshotCreateView(CreateView):
    model = Snapshot
    form_class = SnapshotForm
    fields = ['name', 'timestamp']
    template_name = "snapshots/snapshot_create.html"
    success_url = reverse_lazy("snapshot_list")

    def __init__(self, **kwargs):
        return super(SnapshotCreateView, self).__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        return super(SnapshotCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(SnapshotCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(SnapshotCreateView, self).post(request, *args, **kwargs)

    def get_form_class(self):
        return super(SnapshotCreateView, self).get_form_class()

    def get_form(self, form_class):
        return super(SnapshotCreateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(SnapshotCreateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(SnapshotCreateView, self).get_initial()

    def form_invalid(self, form):
        return super(SnapshotCreateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(SnapshotCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(SnapshotCreateView, self).get_context_data(**kwargs)
        return ret

    def render_to_response(self, context, **response_kwargs):
        return super(SnapshotCreateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(SnapshotCreateView, self).get_template_names()

    def get_success_url(self):
        return reverse("snapshot_detail", args=(self.object.pk,))


class SnapshotUpdateView(UpdateView):
    model = Snapshot
    form_class = SnapshotForm
    fields = ['name', 'timestamp']
    template_name = "snapshots/snapshot_update.html"
    initial = {}
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = "snapshot"

    def __init__(self, **kwargs):
        return super(SnapshotUpdateView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(SnapshotUpdateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(SnapshotUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(SnapshotUpdateView, self).post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(SnapshotUpdateView, self).get_object(queryset)

    def get_queryset(self):
        return super(SnapshotUpdateView, self).get_queryset()

    def get_slug_field(self):
        return super(SnapshotUpdateView, self).get_slug_field()

    def get_form_class(self):
        return super(SnapshotUpdateView, self).get_form_class()

    def get_form(self, form_class):
        return super(SnapshotUpdateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(SnapshotUpdateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(SnapshotUpdateView, self).get_initial()

    def form_invalid(self, form):
        return super(SnapshotUpdateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(SnapshotUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(SnapshotUpdateView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(SnapshotUpdateView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(SnapshotUpdateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(SnapshotUpdateView, self).get_template_names()

    def get_success_url(self):
        return reverse("snapshot_detail", args=(self.object.pk,))


class SnapshotDeleteView(DeleteView):
    model = Snapshot
    template_name = "snapshots/snapshot_delete.html"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = "snapshot"

    def __init__(self, **kwargs):
        return super(SnapshotDeleteView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(SnapshotDeleteView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        return super(SnapshotDeleteView, self).post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super(SnapshotDeleteView, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(SnapshotDeleteView, self).get_object(queryset)

    def get_queryset(self):
        return super(SnapshotDeleteView, self).get_queryset()

    def get_slug_field(self):
        return super(SnapshotDeleteView, self).get_slug_field()

    def get_context_data(self, **kwargs):
        ret = super(SnapshotDeleteView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(SnapshotDeleteView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(SnapshotDeleteView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(SnapshotDeleteView, self).get_template_names()

    def get_success_url(self):
        return reverse("snapshot_list")
