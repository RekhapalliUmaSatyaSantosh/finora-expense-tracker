from django.db import models

# Create your models here.
class Users(models.Model):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    password=models.CharField(max_length=100)

class Category(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=40)
    desc=models.TextField()

class Expenses(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    date = models.DateField()
    payment_method = models.CharField(max_length=30)
    
class Budget(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    class Meta:
        unique_together = ('user', 'month', 'year')
    def __str__(self):
        return f"{self.user.username} - {self.month}/{self.year}"
    
class Income(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    source = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200, blank=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.source} - ₹{self.amount}"