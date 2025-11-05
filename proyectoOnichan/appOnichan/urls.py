from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('tienda/', views.pagina2, name='shop'),
    path('dashboard/', views.pagina4, name='dashboard'),
    path('orders/', views.pagina3, name='orders'),
    path('dashboard/product/<str:product_label>/', views.product_detail, name='product_detail'),
    path('dashboard/detail/<str:chart>/<str:label>/', views.dashboard_detail, name='dashboard_detail'),
    # API endpoints used by JS (minimal implementations)
    path('api/orders/', views.api_orders, name='api_orders'),
    path('api/orders/<int:order_id>/update/', views.api_order_update, name='api_order_update'),
    path('contact/', views.contact, name='contact'),
    path('checkout/', views.checkout, name='checkout'),
]
