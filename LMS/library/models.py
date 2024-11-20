from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class books(models.Model):
  title=models.CharField(max_length=200)
  author=models.CharField(max_length=200)
  image=models.ImageField(upload_to='photos/',blank=True,null=True)
  status=models.BooleanField(default=True)

  def __str__(self):
    return self.title
  
class mybag(models.Model):
   book=models.ForeignKey(books,on_delete=models.CASCADE)
   user=models.ForeignKey(User,on_delete=models.CASCADE)
  #  image=models.ImageField(upload_to='photos/',blank=True,null=True)


class Checkout(models.Model):
  book=models.ForeignKey(books,on_delete=models.CASCADE,null=True)
  reader=models.ForeignKey(User,on_delete=models.CASCADE)
  checkout_date=models.DateTimeField()
  return_due_date=models.DateTimeField()
  returned=models.BooleanField(default=False)

 


  
  





