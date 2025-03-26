from django.db import models

from django.db import models


class Customer(models.Model):
    SEGMENT_CHOICES = [
        ('A1', 'Nhân viên văn phòng, chủ doanh nghiệp (36-45 tuổi) có mức thu nhập cao'),
        ('A2', 'Nhân viên văn phòng, Freelancer ở Miền Bắc (25-35 tuổi)'),
        ('A3', 'Sinh viên, nhân viên văn phòng, freelancer (18-24 tuổi)'),
        ('B1', 'Người làm kinh doanh hoặc văn phòng (45+ tuổi) có thu nhập trung bình'),
        ('B2', 'Người làm nghề tự do hoặc nhân viên văn phòng (36-45 tuổi)'),
        ('B3', 'Người làm nghề tự do hoặc nhân viên văn phòng (25-35 tuổi) ở Miền Bắc'),
        ('C1', 'Sinh viên đi làm thêm, nhân viên mới đi làm (20-29 tuổi)'),
        ('C2', 'Nhân viên văn phòng, người làm việc tự do (30-45 tuổi) ở miền Bắc'),
        ('C3', 'Người mua để uống không có mục đích cụ thể (45+)'),
    ]
    
    customer_id = models.CharField(max_length=10, primary_key=True) 
    name = models.CharField(max_length=100, null=True, blank=True)  
    segment_code = models.CharField(max_length=3, choices=SEGMENT_CHOICES) 

    def __str__(self):
        return self.name or self.customer_id

class ProductGroup(models.Model):
    GROUP_CHOICES = [
        ('BOT', 'Bột'),
        ('SET', 'Set trà'),
        ('THO', 'Trà hoa'),
        ('TTC', 'Trà củ, quả sấy'),
        ('TMX', 'Trà mix'),
    ]
    
    group_code = models.CharField(max_length=3, primary_key=True, choices=GROUP_CHOICES)  
    group_name = models.CharField(max_length=50)  
    def __str__(self):
        return self.group_name

class Product(models.Model):
    product_code = models.CharField(max_length=10, primary_key=True)  
    name = models.CharField(max_length=100) 
    group = models.ForeignKey(ProductGroup, on_delete=models.CASCADE)  
    unit_price = models.IntegerField() 

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.CharField(max_length=10, primary_key=True) 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) 
    order_time = models.DateTimeField() 
    def __str__(self):
        return self.order_id


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    quantity = models.IntegerField()  

    def __str__(self):
        return f"{self.order.order_id} - {self.product.name}"

    @property
    def total_price(self):
        return self.quantity * self.product.unit_price

    class Meta:
        unique_together = ('order', 'product') 
