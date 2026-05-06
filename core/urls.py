from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_redirect, name='dashboard_redirect'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_dashboard/staff/add/', views.add_staff, name='add_staff'),
    path('admin_dashboard/order/add/', views.create_order, name='create_order'),
    path('admin_dashboard/order/<int:order_id>/delete/', views.delete_order, name='delete_order'),
    path('customer/order/<int:order_id>/request_delivery/', views.request_delivery, name='request_delivery'),
]
