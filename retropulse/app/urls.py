from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalogo/', views.catalog, name='catalog'),
    path('producto/<int:cod_producto>/', views.product_detail, name='product_detail'),
    path('nosotros/', views.about, name='about'),
    path('carrito/', views.cart_detail, name='cart_detail'),
    path('acceso/', views.auth_view, name='login'), # Ruta de Login/Signup unificados
    path('registro/', views.auth_view, name='register'),
    path('salir/', views.logout_view, name='logout'),
    path('inspector/', views.db_inspector, name='db_inspector'), # Acceso exclusivo de Admin
    path('inspector/eliminar/<int:cod_producto>/', views.eliminar_producto, name='eliminar_producto'),
]