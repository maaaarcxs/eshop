from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, CartItem, Cart, Category, Brand
from django.views.generic import ListView
from django.contrib import messages


def get_cart(request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            session_key = request.session.session_key
        if session_key:
            session_cart = Cart.objects.filter(session_key=session_key).first()
        if session_cart:
            for item in session_cart.items.all():
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=item.product)
                if not created:
                    cart_item.quantity += item.quantity
                else:
                    cart_item.quantity = item.quantity
                    cart_item.save()
                    session_cart.delete()
                return cart
        else:
            session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart


class ItemListView(ListView):
    model = Item
    template_name = "home.html"
    context_object_name = "items"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        category_id = self.request.GET.get("category")
        brand_id = self.request.GET.get("brand")
        search_query = self.request.GET.get("q")
        if category_id:
            qs = qs.filter(category_id=category_id)
        if brand_id:
            qs = qs.filter(brand_id=brand_id)
        if search_query:
            qs = qs.filter(model__icontains=search_query)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["brands"] = Brand.objects.all()
        context["selected_category"] = self.request.GET.get("category")
        context["selected_brand"] = self.request.GET.get("brand")
        context["search_query"] = self.request.GET.get("q")
        return context

    # def get_cart(request):
    #     if request.user.is_authenticated:
    #         cart, created = Cart.objects.get_or_create(user=request.user)
    #         session_key = request.session.session_key
    #     if session_key:
    #         session_cart = Cart.objects.filter(session_key=session_key).first()
    #     if session_cart:
    #         for item in session_cart.items.all():
    #             cart_item, created = CartItem.objects.get_or_create(cart=cart, product=item.product)
    #             if not created:
    #                 cart_item.quantity += item.quantity
    #             else:
    #                 cart_item.quantity = item.quantity
    #                 cart_item.save()
    #                 session_cart.delete()
    #             return cart
    #     else:
    #         session_key = request.session.session_key
    #     if not session_key:
    #         request.session.create()
    #         session_key = request.session.session_key
    #         cart, created = Cart.objects.get_or_create(session_key=session_key)
    #     return cart

class CartView(View):
    def get(self, request):
        # cart = ItemListView.get_cart(request)
        cart = get_cart(request)
        items = cart.items.select_related("product")
        total = cart.total_price()
        return render(request, "cart.html", {"cart": cart, "items": items, "total": total})

class AddToCartView(View):
    def post(self, request, item_id):
        cart = get_cart(request)
        product = get_object_or_404(Item, id=item_id)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += 1
        else:
            item.quantity = 1
            item.save()
            messages.success(request, f"Товар '{product.model}' добавлен в корзину.")
        return redirect("cart")

class RemoveFromCartView(View):
    def post(self, request, item_id):
        cart = get_cart(request)
        item = cart.items.filter(product_id=item_id).first()
        if item:
            item.delete()
            messages.success(request, f"Товар '{item.product.model}' удален из корзины.")
            return redirect("cart")

class UpdateCartItemView(View):
    def post(self, request, item_id):
        cart = get_cart(request)
        item = cart.items.filter(product_id=item_id).first()
        # if item:
        #     action = request.POST.get("action")
        if not item:
            messages.error(request, "Товар не найден в корзине.")
            return redirect("cart")
        action = request.POST.get("action")

        if action == "increase":
            item.quantity += 1
            item.save()
            messages.success(request, f"Количество товара '{item.product.model}' увеличено")
        elif action == "decrease":
            item.quantity -= 1
            if item.quantity <= 0:
                item.delete()
                messages.success(request, f"Товар '{item.product.model}' удален из корзины")
            else:
                item.save()
                messages.success(request, f"Количество товара '{item.product.model}' уменьшено")
        return redirect("cart")

class ClearCartView(View):
    def post(self, request):
        cart = get_cart(request)
        cart.items.all().delete()
        messages.success(request, "Корзина очищена")
        return redirect("cart")

class ItemDetailView(View):
    def get(self, request, pk):
        item = get_object_or_404(Item, id=pk)
        return render(request, "item_detail.html", {"item": item})