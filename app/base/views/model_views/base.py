from django.core.paginator import Paginator
from django.db.models import Model, Q, QuerySet, Value as V
from django.db.models.functions import Concat
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.edit import FormMixin

from app.base.templatetags.url_utils import url_with_formatter, UrlFormatObject

from typing import (
    Generic, TypeVar, Union, Type, List, Dict, Any, Tuple, Optional,
    Sequence, Literal, TypedDict)


# --------------------------------------------
#  Types
# --------------------------------------------

M = TypeVar('M', bound=Model)
ListFilterOption = Dict[str, str]  # {GET-key: model-query-filter-key}
ListColumnsOption = List[str]
RenderOptions = Dict[str, Dict[str, Any]]
SearchQueryOption = List[str]
ViewsOption = Dict[str, str]
FieldsOption = Union[Sequence[str], Literal['__all__'], None]
OnSuccessOption = UrlFormatObject
BreadcrumbEntry = Tuple[str, Optional[UrlFormatObject]]  # (title, href-url)


class ToolbarButtonType(TypedDict, total=False):
    icon: Optional[str]
    label: str
    href: str  # use either href or path, not both. href takes precedence
    path: UrlFormatObject


# --------------------------------------------
#  Base Options
#
#  - ViewOptions (ListView)
#    - SubviewOfListOptions (DetailView)
#      - SubviewWithEditOptions (CreateView, UpdateView, DeleteView)
# --------------------------------------------

class ViewOptions(Generic[M], ContextMixin):
    model: Type[M]  # must be declared for each View separately
    object: M  # populated by django
    title: str = ''  # used for h1 and button titles
    icon = 'database'  # please override
    views: ViewsOption = {}
    detail_fields: FieldsOption = '__all__'
    detail_render: RenderOptions = {}
    list_filter: ListFilterOption = {}
    list_columns: ListColumnsOption = []
    list_render: RenderOptions = {}
    toolbar_buttons: List[ToolbarButtonType] = []

    def get_breadcrumbs(self) -> List[BreadcrumbEntry]:
        return [(self.get_title(), None)]

    def get_title(self) -> str:
        return self.title.format(*[self] * 9) if self.title else \
            (self.model._meta.verbose_name_plural or '')

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)  # type: ignore
        context['model_verbose_name'] = self.model._meta.verbose_name \
            if hasattr(self, 'model') else None
        context['breadcrumbs'] = self.get_breadcrumbs()
        context['icon'] = self.icon
        context['title'] = self.title.format(*[self] * 9) if self.title else \
            self.model._meta.verbose_name_plural
        context['views'] = self.views
        context['toolbar_buttons'] = self.toolbar_buttons
        context['detail_fields'] = self.detail_fields
        context['detail_render'] = self.detail_render
        context['list_render'] = self.list_render
        context['list_columns'] = self.list_columns
        context['list_filter'] = self.list_filter
        return context


class SubviewOfListOptions(ViewOptions[M]):
    def get_breadcrumbs(self) -> List[BreadcrumbEntry]:
        active_page_breadcrumb = super().get_breadcrumbs()
        parent = self.views.get('list')
        if not parent:
            return active_page_breadcrumb
        title = self.model._meta.verbose_name_plural or '-?-'
        return [(title, parent)] + active_page_breadcrumb


class SubviewWithEditOptions(
        SubviewOfListOptions[M], TemplateResponseMixin, FormMixin):
    on_success: OnSuccessOption = ''  # format source is: self.object

    def get_success_url(self) -> str:
        prev = self.request.GET.get('prev')
        if isinstance(self, DeleteView):
            obj_url = getattr(self.object, 'get_absolute_url', lambda: None)()
            if obj_url == prev:
                prev = None  # do not redirect to detail page after delete
        if prev:
            return prev
        target = self.on_success
        if not target:
            return super().get_success_url()
        return url_with_formatter(target, self.object)


# --------------------------------------------
#  List Options
# --------------------------------------------

class ModelListView(ViewOptions[M], ListView):
    template_name = 'generic/list.html'
    paginate_by = 50
    search_fields: SearchQueryOption = []

    def get_list_filter(self) -> Optional[Dict[str, str]]:
        rv = {}
        for get_key, model_key in self.list_filter.items():
            val = self.request.GET.get(get_key, None)
            if val is not None:
                rv[model_key] = val or None
        # allow to search records with ?q=
        search_query = self.request.GET.get('q')
        if search_query and self.search_fields:
            rv['search_qry_fld__icontains'] = search_query
        return rv

    def _annotate_with_search_query(self) -> QuerySet:
        ''' called if and only if filters are active '''
        # self.get_queryset()  or  self.model.objects ?
        query = self.get_queryset()
        if self.search_fields:
            search_field = Concat(*[
                y for x in self.search_fields for y in (V(' '), x)
            ][1:])  # ignore first space
            return query.annotate(search_qry_fld=search_field)
        return query

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)  # type: ignore

        # Apply filter if specified & active
        list_filter = self.get_list_filter()
        if list_filter:
            sort_order = self.ordering or self.model._meta.ordering or []
            filtered_objs = self._annotate_with_search_query().filter(
                Q(**list_filter)).order_by(*sort_order)
            pagination = Paginator(filtered_objs, self.paginate_by)
            preferred_page = int(self.request.GET.get('page', 1))
            actual_page = min(max(preferred_page, 1), pagination.num_pages)
            page_obj = pagination.page(actual_page)
            context['object_list'] = page_obj
            context['page_obj'] = page_obj
            search_query = list_filter.get('search_qry_fld__icontains')
            if search_query:
                context['active_search_query'] = search_query
                context['breadcrumbs'] = [
                    (context['title'], self.views.get('list', 'index')),
                    (f'Suchergebnisse für "{search_query}"', None)
                ]
        return context


# --------------------------------------------
#  Detail Options
# --------------------------------------------

class ModelDetailView(SubviewOfListOptions[M], DetailView):
    template_name = 'generic/detail.html'
    title = '{.object}'


# --------------------------------------------
#  Create Options
# --------------------------------------------

class ModelCreateView(SubviewWithEditOptions[M], CreateView):
    template_name = 'generic/create.html'
    title = '{.model._meta.verbose_name} anlegen'
    fields: FieldsOption = '__all__'  # you probably want to override that

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['submit_label'] = f'{self.model._meta.verbose_name} anlegen'
        return context

    # def get_success_url(self) -> str:
    #     prev = self.request.GET.get('prev')
    #     if prev:
    #         return prev
    #     return super().get_success_url()


# --------------------------------------------
#  Update Options
# --------------------------------------------

class ModelUpdateView(SubviewWithEditOptions[M], UpdateView):
    template_name = 'generic/update.html'
    title = '"{.object}" bearbeiten'
    fields: FieldsOption = '__all__'  # you probably want to override that


# --------------------------------------------
#  Delete Options
# --------------------------------------------

class ModelDeleteView(SubviewWithEditOptions[M], DeleteView):
    template_name = 'generic/delete.html'
    title = '"{.object}" löschen'
