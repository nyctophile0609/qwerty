from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import datetime
import os
import shutil


class MaterialModel(models.Model):
    name=models.CharField(max_length=150)
    
class ProductModel(models.Model):
    name=models.CharField(max_length=150)
    code=models.CharField(max_length=150)

class ProductMaterialModel(models.Model):
    product_id=models.ForeignKey(ProductModel,on_delete=models.SET_NULL,null=True)
    material_id=models.ForeignKey(MaterialModel,on_delete=models.SET_NULL,null=True)
    quantity=models.DecimalField(max_digits=32,decimal_places=2)


class WarehouseModel(models.Model):
    material_id=models.ForeignKey(MaterialModel,on_delete=models.SET_NULL,null=True)
    remainder=models.DecimalField(max_digits=32,decimal_places=2)
    free=models.DecimalField(max_digits=32,decimal_places=2)
    price=models.DecimalField(max_digits=32,decimal_places=2)
    created_date=models.DateTimeField(auto_now_add=True)

    class Meta:
            ordering = ['created_date']

class TemporaryModel(models.Model):
    product_id=models.ForeignKey(ProductModel,on_delete=models.SET_NULL,null=True)
    quantity=models.DecimalField(max_digits=32,decimal_places=2)
    created_date=models.DateTimeField(auto_now_add=True)
    class Meta:
            ordering = ['created_date']