from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('index', views.index,name='index'),
    path('cancellation', views.cancellation,name='cancellation'),
    path('policy', views.policy,name='policy'),
    path('Terms_and_conditions', views.Terms_and_conditions,name='Terms_and_conditions'),
    path('shipping', views.shipping,name='shipping'),
    path('about', views.about,name='about'),
    path('contact', views.contact,name='contact'),
    path('cart', views.cart,name='cart'),
    path('success', views.success, name='success'),
    path('blog', views.blog,name='blog'),
    path('checkout', views.checkout,name='checkout'),
    path('login/', views.login_view,name='login'),
    path('logout', views.logout_view,name='logout_view'),
    path('admindashboard/', views.admindashboard,name='admindashboard'),
    path('registered-users-count/', views.registered_users_count_view, name='registered_users_count'),
    path('checkout/', views.checkout_list, name='checkout_list'),

    path('add_category', views.add_category,name='add_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('category_details', views.category_details,name='category_details'),

    path('add_product', views.add_product,name='add_product'),
    path('product_data', views.product_data,name='product_data'),
    path('save_customer/', views.save_customer,name='save_customer'),
    path('add-to-cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('category/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('clear-cart/', views.clear_cart, name='clear-cart'),
    path('update_quantity/<int:item_id>/<str:action>/', views.update_quantity, name='update_quantity'),
    path('orders/', views.orders,name='orders'),
    path('dash/', views.dash, name='dash'),
    path('save_farmer/', views.save_farmer,name='save_farmer'),
    path('farmer_login/', views.farmer_login,name='farmer_login'),
    path('Dharwad/', views.Dharwad, name='Dharwad'),
    path('Bengaluru/', views.Bengaluru, name='Bengaluru'),
    path('Raichur/', views.Raichur, name='Raichur'),
    path('Koppal/', views.Koppal, name='Koppal'),





]
