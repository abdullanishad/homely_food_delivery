from django.urls import path
from .views import ItemListView, CartView, item_detail, CheckoutView, order_success, SellerItemsFilterView, MyOrderView
from .views import category_cakes


urlpatterns = [
    path('', ItemListView.as_view(), name='home'),
    path('item/<slug>/', item_detail, name='item-detail'),
    path('order_success/', order_success, name='order-success'),
    # path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('myorder/', MyOrderView.as_view(), name='myorder'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('sellerpost/<str:name>', SellerItemsFilterView.as_view(), name='seller-items-filter'),
]

urlpatterns += [
    path('cakes', category_cakes, name='category-cakes')

]
