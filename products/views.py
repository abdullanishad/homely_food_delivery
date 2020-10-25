import random
import string

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from django.utils import timezone
from django.views.generic import ListView, DetailView, View

from .forms import OrderItemForm, CheckoutForm
from .models import Item, OrderItem, Order, Seller


class ItemListView(ListView):
    model = Item
    paginate_by = 10


# class ItemDetailView(DetailView):
#     model = Item
#     form = OrderItemForm


# @login_required
# def add_to_cart(request, slug):
#     item = get_object_or_404(Item, slug=slug)
#     order_list = Order.objects.filter(user=request.user, ordered=False)
#     if order_list.exists():
#         order = order_list[0]
#         new_order_item = OrderItem.objects.create(
#             user=request.user, order_id=order,
#             item=item,
#             # size = size, quantity=quantity, message=message, instructions=instructions,
#             ordered=False
#         )
#         new_order_item.save()
#         messages.info(request, "This item was added to your cart.")
#         return redirect("item-list", slug=slug)
#     else:
#         ordered_date = timezone.now()
#         order = Order.objects.create(
#             user=request.user, ordered_date=ordered_date)
#         order.save()
#         new_order_item = OrderItem.objects.create(
#             user=request.user, order_id=order, item=item,
#             # size=size, quantity=quantity, message=message, instructions=instructions,
#             ordered=False
#         )
#         new_order_item.save()
#         messages.info(request, "This item was added to your cart.")
#         return redirect("item-list", slug=slug)


def item_detail(request, slug):
    item = get_object_or_404(Item, slug=slug)
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            message = form.cleaned_data['message']
            instructions = form.cleaned_data['instructions']
            order_list = Order.objects.filter(user=request.user, ordered=False)
            if order_list.exists():
                order = order_list[0]
                new_order_item = OrderItem.objects.create(
                    user=request.user, order_id=order,
                    item=item,
                    quantity=quantity, message=message, instructions=instructions,
                    ordered=False,
                )
                new_order_item.total_orderitem_price = int(quantity * item.price)
                order.total_order_price += new_order_item.total_orderitem_price
                new_order_item.save()
                order.save()
                messages.info(request, "This item was added to your cart.")
                return redirect("item-detail", slug=slug)
            else:
                ordered_date = timezone.now()
                order = Order.objects.create(
                    user=request.user, ordered_date=ordered_date)
                new_order_item = OrderItem.objects.create(
                    user=request.user, order_id=order, item=item,
                    quantity=quantity, message=message, instructions=instructions,
                    ordered=False
                )
                new_order_item.total_orderitem_price = int(quantity * item.price)
                order.total_order_price += new_order_item.total_orderitem_price
                new_order_item.save()
                order.save()
                messages.info(request, "This item was added to your cart.")
                return redirect("item-detail", slug=slug)
    else:
        form = OrderItemForm()
    context = {
        'form': form,
        'item': item,
    }

    return render(request, 'products/item_detail.html', context)



class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order_item = OrderItem.objects.filter(user=self.request.user, ordered=False,)
            total = 0
            for item in order_item:
                sigle_item_total = 0
                sigle_item_total = item.item.price * item.quantity
                total += sigle_item_total
            total += 50
            context = {
                'object': order_item,
                'total': total
            }
            return render(self.request, 'products/cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")

    # def post(self, *args, **kwargs):
    #     form = CheckoutForm(self.request.POST or None)
    #     try:
    #         order = Order.objects.filter(user=self.request.user, ordered=False, )
    #         order_items = OrderItem.objects.filter(user=self.request.user, ordered=False,)
    #         if form.is_valid():
    #
    #         form = OrderItemForm(self.request.POST)
    #
    #         order.ordered = True
    #         order.save()
    #
    #         for item in order_items:
    #             item.ordered = True
    #             item.save()
    #     except ObjectDoesNotExist:
    #         messages.warning(self.request, "cart is empty")
    #         return redirect("/")


class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order_item = OrderItem.objects.filter(user=self.request.user, ordered=False,)
            form = CheckoutForm()
            total = 0
            for price in order_item:
                total += price.item.price
            total += 50
            context = {
                'form': form,
                'object': order_item,
                'total': total
            }
            return render(self.request, 'products/checkout.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False, )
            order_items = OrderItem.objects.filter(user=self.request.user, ordered=False,)
            if order:
                if form.is_valid():
                    order.fullname = form.cleaned_data['fullname']
                    order.delivery_date = form.cleaned_data['delivery_date']
                    order.address = form.cleaned_data['address']
                    order.location = form.cleaned_data['location']
                    order.ordered=True
                    # total = 0
                    # for price in order_items:
                    #     total += int(price.total_item_price)
                    # order.total_order_price = total
                    order.save()

                    for item in order_items:
                        item.ordered = True
                        item.save()
                    messages.success(self.request, "Your order was successful!")
                    return redirect("order-success")

        except ObjectDoesNotExist:
            messages.warning(self.request, "cart is empty")
            return redirect("cart")

        messages.warning(self.request, "oops! enter valid input")
        return redirect("checkout")


def order_success(request):
    order = Order.objects.filter(user=request.user).order_by('-ordered_date')[0]
    return render(request, 'products/order_success.html', {'order': order })


def category_cakes(request):
    context = Item.objects.filter(category='cakes')
    return render(request, 'products/category/cakes.html', {'context': context})


class SellerItemsFilterView(ListView):
    model = Item
    template_name = 'products/selleritems.html'
    paginate_by = 5

    def get_queryset(self):
        seller = get_object_or_404(Seller, name=self.kwargs.get('name'))
        return Item.objects.filter(seller=seller)


class MyOrderView(ListView):
    model = OrderItem
    template_name = 'products/myorder.html'
    paginate_by = 5

    def get_queryset(self):
        return OrderItem.objects.filter(user=self.request.user, delivered=False)