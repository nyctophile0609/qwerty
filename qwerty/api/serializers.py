from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import *
from .serializers import *



class MaterialModelSerializer(ModelSerializer):
    class Meta:
        model = MaterialModel
        fields = ['id', 'name']

class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ['id', 'name','code']

class ProductMaterialModelSerializer1(ModelSerializer):
    product_id = ProductModelSerializer(read_only=True) 
    material_id = MaterialModelSerializer(read_only=True)  
    class Meta:
        model = ProductMaterialModel
        fields = ['id', 'product_id', 'material_id', 'quantity']

class ProductMaterialModelSerializer2(ModelSerializer):
    class Meta:
        model = ProductMaterialModel
        fields = ['id', 'product_id', 'material_id', 'quantity']

class WarehouseModelSerializer1(ModelSerializer):
    material_id = MaterialModelSerializer(read_only=True) 

    class Meta:
        model = WarehouseModel
        fields = ['id', 'material_id', 'remainder',"free", 'price']


class WarehouseModelSerializer2(ModelSerializer):
    class Meta:
        model = WarehouseModel
        fields = ['id', 'material_id', 'remainder', 'price']
        
    def create(self, validated_data):
        new_object=WarehouseModel.objects.create(**validated_data)
        new_object.free=validated_data.get("remainder")
        new_object.save()
        return new_object

    def update(self, instance, validated_data):
        instance.free=validated_data.get("remainder")
        return super().update(instance, validated_data)



class TemporaryModelSerializer(ModelSerializer):
    class Meta:
        model = TemporaryModel
        fields = "__all__"



class ProductInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)

class SpecialFunctionInputSerializer(serializers.Serializer):
    products = ProductInputSerializer(many=True, required=True)
