from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(verbose_name="Название", max_length=100)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"


class Brand(models.Model):
    name = models.CharField(verbose_name="Бренд", max_length=100)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Марка"
        verbose_name_plural = "Марки"
    

class Item(models.Model):
    photo = models.ImageField(verbose_name="Фото", upload_to="items/")
    model = models.CharField(verbose_name="модель", max_length=100)
    price = models.IntegerField(verbose_name="цена")
    description = models.TextField(verbose_name="Описание", max_length=1500)
    stock = models.BooleanField(verbose_name="В наличии")
    category = models.ForeignKey(Category, verbose_name="Категория товара", on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, verbose_name="Бренд", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.brand}  {self.model}  {self.price}  {self.stock}  {self.photo}"
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        if self.user:
            return f"{self.user.username}"
        return f"{self.session_key}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.price * self.quantity
    
    def __str__(self):
        return f"{self.cart}  {self.product}  {self.quantity}"