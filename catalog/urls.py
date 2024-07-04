from django.urls import path
from django.views.decorators.cache import never_cache

from catalog.views import ProductListView, ProductDetailView, ProductUpdateView, ProductCreateView, \
    VersionDetailView, VersionCreateView, VersionUpdateView, ProductDeleteView

app_name = 'catalog'

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('product/<int:pk>', never_cache(ProductDetailView.as_view()), name='product_detail'),
    path('create/', never_cache(ProductCreateView.as_view()), name='create_product'),
    path('update/<int:pk>', never_cache(ProductUpdateView.as_view()), name='update_product'),
    path('version/<int:version_id>/', VersionDetailView.as_view(), name='version-detail'),
    path('version/form/<int:pk>/', never_cache(VersionCreateView.as_view()), name='version-form'),
    path('version/edit/<int:pk>/', never_cache(VersionUpdateView.as_view()), name='version-edit'),
    path('product/delete/<int:pk>/', never_cache(ProductDeleteView.as_view()), name='product-delete'),
    path('product/edit/<int:pk>/', never_cache(ProductUpdateView.as_view()), name='product-edit'),

]

