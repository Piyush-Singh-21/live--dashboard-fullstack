from django.db import models
class Customer(models.Model):
    name=models.CharField(max_length=120); email=models.EmailField(unique=True); phone=models.CharField(max_length=20); created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name
class Mechanic(models.Model):
    name=models.CharField(max_length=120); phone=models.CharField(max_length=20); status=models.CharField(max_length=30,default="Available"); jobs_completed=models.PositiveIntegerField(default=0)
    def __str__(self): return self.name
class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING="Pending"; ASSIGNED="Assigned"; ON_THE_WAY="Mechanic On The Way"; COMPLETED="Completed"; CANCELLED="Cancelled"
    reference=models.CharField(max_length=20,unique=True); customer=models.ForeignKey(Customer,on_delete=models.PROTECT,related_name="bookings"); mechanic=models.ForeignKey(Mechanic,null=True,blank=True,on_delete=models.SET_NULL,related_name="bookings"); vehicle=models.CharField(max_length=120); service=models.CharField(max_length=80); status=models.CharField(max_length=30,choices=Status.choices,default=Status.PENDING); amount=models.DecimalField(max_digits=10,decimal_places=2); scheduled_at=models.DateTimeField(db_index=True); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=["-scheduled_at"]
    def __str__(self): return self.reference
