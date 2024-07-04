from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

from catalog.forms import ProductCreateForm, ProductUpdateForm, VersionCreateForm, VersionUpdateForm, ProductForm
from catalog.models import Product, Version
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, CreateView, DeleteView

from catalog.services import get_cached_categories


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['products']
        active_versions = {}

        for product in products:
            active_version = product.version_set.filter(current_version=True).first()
            if active_version is None:
                active_versions[product.pk] = None
            else:
                active_versions[product.pk] = active_version

        context['active_versions'] = active_versions
        context['categories'] = get_cached_categories()
        return context


@method_decorator(login_required(login_url=reverse_lazy('user:login')), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    @method_decorator(cache_page(60 * 15))  # Применение декоратора к методу dispatch
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['categories'] = get_cached_categories()
        return context_data


@method_decorator(login_required(login_url=reverse_lazy('user:login')), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        active_versions = {}

        for product in products:
            active_version = product.version_set.filter(current_version=True).first()
            if active_version is None:
                active_versions[product.pk] = None
            else:
                active_versions[product.pk] = active_version

        context['active_versions'] = active_versions

        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.is_banned = any(word in form.cleaned_data['name'].lower() or
                                      word in form.cleaned_data['description'].lower()
                                      for word in ['casino', 'cryptocurrency', 'crypto', 'exchange', 'cheap',
                                                   'free', 'scam', 'police', 'radar'])
        form.instance.last_modified_date = timezone.now()
        return super().form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy('user:login')), name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = 'catalog/product_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['products']
        active_versions = {}

        for product in products:
            active_version = product.version_set.filter(current_version=True).first()
            if active_version is None:
                active_versions[product.pk] = None
            else:
                active_versions[product.pk] = active_version

        context['active_versions'] = active_versions
        return context

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        return self.object

    def get_success_url(self):
        return reverse_lazy('catalog:product-detail', kwargs={'pk': self.object.pk})


@method_decorator(login_required(login_url=reverse_lazy('user:login')), name='dispatch')
class ContactDetailView(TemplateView):
    template_name = 'catalog/contacts.html'


@method_decorator(login_required(login_url=reverse_lazy('user:login')), name='dispatch')
class VersionDetailView(DetailView):
    model = Version
    template_name = 'catalog/version_detail.html'
    context_object_name = 'version'

    def get_object(self, queryset=None):
        version_id = self.kwargs.get('version_id')
        return Version.objects.get(id=version_id)


@method_decorator(login_required(login_url=reverse_lazy('user:login')), name='dispatch')
class VersionCreateView(CreateView):
    model = Version
    form_class = VersionCreateForm
    template_name = 'catalog/version_form.html'

    def form_valid(self, form):
        product = get_object_or_404(Product, id=self.kwargs.get('pk'))
        form.instance.product = product
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:home')


@method_decorator(login_required(login_url=reverse_lazy('user:login')), name='dispatch')
class VersionUpdateView(UpdateView):
    model = Version
    template_name = 'catalog/version_form.html'
    form_class = VersionUpdateForm

    def get_success_url(self):
        return reverse('catalog:version-detail', kwargs={'version_id': self.object.pk})


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('products:home')

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("У вас нет прав на редактирование этого товара.")
        return super().handle_no_permission()

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('products:home')

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("У вас нет прав на удаление этого товара.")
        return super().handle_no_permission()

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if hasattr(self.object, 'owner') and self.request.user == self.object.owner:
            return super().delete(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("У вас нет прав на удаление этого товара.")
