from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Cities(models.Model):
    city = models.CharField(blank=False, null=False,
                            max_length=100, unique=True)
    
    def __str__(self):
        return self.city
    
class Car(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    car_no=models.CharField(max_length=20,blank=False, null=False)
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='car_images/', null=True, blank=True)
   
class drivers(models.Model):
    gender = (
        ('male','male'),
        ('female', 'female'),
    )
    image=models.ImageField(upload_to='media',null=True, blank=True)
    name=models.CharField(max_length=100,null=True, blank=True)
    gender=models.CharField(max_length=100,choices=gender,null=True, blank=True)
    age=models.IntegerField(null=True, blank=True )
    phone=models.IntegerField( null=True, blank=True)
    licence_no=models.CharField(max_length=20,null=True, blank=True)
    car_no=models.ForeignKey(Car,on_delete=models.CASCADE,max_length=20,blank=False, null=False)
    
    def __str__(self):
        return f"{self.name} {self.car_no}"

 
# models.py

class PreRegistration(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password1 = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)
    otp = models.CharField(max_length=10)
    


# class CarRental(models.Model):
#     car = models.ForeignKey(Car, on_delete=models.CASCADE)
#     pickup_date = models.DateField()
#     delivery_date = models.DateField()
#     username=models.ForeignKey(PreRegistration,on_delete=models.CASCADE)
#     distance_traveled = models.DecimalField(max_digits=5, decimal_places=2)
    
#     # def save(self, *args, **kwargs):
#     #     self.total_amount = self.rental_price * self.distance_traveled
#     #     super().save(*args, **kwargs)
#     @property
#     def market_cap(self):
#         total=self.rental_price * self.distance_traveled
#         return total
    
#     def __str__(self):
#         return f"Rental of {self.car.brand} {self.car.model} from {self.pickup_date} to {self.delivery_date}"
class CarRental(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
  
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    pickup_date = models.DateField()
    delivery_date = models.DateField()
    start= models.CharField(max_length=50,default='bangalore')
  
    to=models.ForeignKey(Cities, on_delete=models.CASCADE)
    distance_traveled = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    
    
        
    @property
    def get_total(self,Car):
        total=Car.rental_price*self.distance_traveled
        return total

    def __str__(self):
        return f"Rental of {self.car.brand} {self.car.model} from {self.pickup_date} to {self.delivery_date}"
