from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauth.models import User

STATUS_CHOICE ={
    ("process","Processing"),
    ("shiped","Shiped"),
    ("delivered","Delivered"), 
}

STATUS ={
    ("draft","Draft"),
    ("disabled","Disabled"),
    ("rejected","Rejected"), 
    ("in_review","In Review"),
    ("published","Published"),
}

RATING ={
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"), 
    (4, "★★★★☆"),
    (5, "★★★★★"),
}


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefgh12345")
    title =models.CharField(max_length=100, default="category title")
    image =models.ImageField(upload_to="category", default="category.jpg")
    
    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" with="50" height="50"/>' %(self.image.url))
    
    def __str__(self):
        return self.title    

class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="vid", alphabet="abcdefgh12345")
    title =models.CharField(max_length=100, default="vendor title")
    image =models.ImageField(upload_to="user_directory_path", default="vendor.jpg")
    description = models.TextField(null=True, blank=True, default="this is a vendor")

    address = models.CharField(max_length=100, default="123 Ange Raphael Douala")
    contact = models.CharField(max_length=100, default="+237 (456)789 108")
    chat_resp_time = models.CharField(max_length=100, default="100")
    shipping_on_time =models.CharField(max_length=100,default="100" )
    authentic_rating = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    waranty_period = models.CharField(max_length=100, default="100")


    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name_plural = "Vendor"

    def vendor_image(self):
        return mark_safe('<img src="%s" with="50" height="50"/>' %(self.image.url))
    
    def __str__(self):
        return self.title 
    

class Tags(models.Model):
    pass

class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="vid", alphabet="abcdefgh12345")
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)



    title =models.CharField(max_length=100, default="product title")
    image =models.ImageField(upload_to="user_directory_path", )
    description = models.TextField(null=True, blank=True, default="this is the product")

    price = models.DecimalField(max_digits=9999999999999, decimal_places=2, default="1.99")
    old_price = models.DecimalField(max_digits=9999999999999, decimal_places=2, default="2.99")

    specifications = models.TextField(null=True, blank=True, )
    tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")
    
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)


    sku = ShortUUIDField(unique=True,length=4, max_length=20, prefix="sku", alphabet="1234567890")
    
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(null=True, blank=True)
   
    class Meta:
        verbose_name_plural = "products"

    def product_image(self):
        return mark_safe('<img src="%s" with="50" height="50"/>' %(self.image.url))
    
    def __str__(self):
        return self.title 
    
    def get_percentage(self):
        new_price = (self.price/self.old_price)*100
        return new_price
    
class ProductImages(models.Model):
    images = models.ImageField(upload_to="product_image", default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"



###################### Cart , Order, OrderItems and Adress ##############

class CartOrder(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=99999999999999, decimal_places=2, default="1.99")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")
    
    
    class Meta:
        verbose_name_plural = "Cart Order"

class CartOrderItems(models.Model):
    order= models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=99999999999999, decimal_places=2, default="1.99")
    total = models.DecimalField(max_digits=99999999999999, decimal_places=2, default="1.99")
     
    class Meta:
        verbose_name_plural = "Cart Order Item"


    def order_img(self):
       return mark_safe('<img src="/media/%s" with="50" height="50"/>' %(self.image.url))
    

 ###################### Product Review, Wishlist, Adress ################


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "product Reviews"

    
    def __str__(self):
        return self.product.title 
    
    def get_rating(self):
        return self.rating
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = " Wishlists"

    
    def __str__(self):
        return self.product.title 
    
class Adress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    adress = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Adress"






