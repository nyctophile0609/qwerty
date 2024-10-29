from rest_framework import viewsets
from rest_framework.decorators import action
from django.db.models import Sum
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


from .models import *
from .serializers import *



class MaterialModelViewSet(viewsets.ModelViewSet):
    queryset = MaterialModel.objects.all()
    serializer_class = MaterialModelSerializer

class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer

class ProductMaterialModelViewSet(viewsets.ModelViewSet):
    queryset = ProductMaterialModel.objects.all()
    serializer_class = ProductMaterialModelSerializer1

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ProductMaterialModelSerializer2
        return ProductMaterialModelSerializer1

class WarehouseModelViewSet(viewsets.ModelViewSet):
    queryset = WarehouseModel.objects.all()
    serializer_class = WarehouseModelSerializer1

    @action(detail=False, methods=["post"])  #Defining a custom action 
    def special_function(self, request):
        new_ones = request.data.get("products")  #getting products from request
        result = []  

        for no in new_ones:
            product=get_object_or_404(ProductModel,id=no["product_id"]) #getting product instance
            qw = {}  
            qw["product_name"] = product.name  
            qw["product_qty"] = no["quantity"] 
            wq = []  

            
            needed_materials = ProductMaterialModel.objects.filter(product_id=product) #getting needed materials for the product
                  
            for nm in needed_materials:
                total_needed_materials = no["quantity"] * nm.quantity  #calculating total needed materials 
                available_materials = WarehouseModel.objects.filter(free__gt=0, material_id=nm.material_id)         #getting available materials in the warehouse


                for am in available_materials:
                    min_materials = min(am.free, total_needed_materials) #getting the available needed material
                    if min_materials < 1:  #breaking the loop if no materials available
                        break
                    total_needed_materials -= min_materials  #reducing total_needed_materials 
                    am.free -= min_materials  #updating the free materials in the warehouse
                    am.save()  #saving updated warehouse object

                    zxc = {
                        "warehouse_id": am.pk,
                        "material_name": am.material_id.name,
                        "qty": min_materials,
                        "price": am.price
                    }
                    wq.append(zxc)  #adding the collected data

                if total_needed_materials > 0:  #checking if more materials needed
                    zxc = {
                        "warehouse_id": None,
                        "material_name": nm.material_id.name,
                        "qty": total_needed_materials,
                        "price": None
                    }
                    wq.append(zxc)#dding unavailable needed material data 

            qw["product_materials"] = wq  #addding materials list to the response
            result.append(qw)  #adding product and warehouse material info to the final response
        
        return Response({"result": result})  #returning the final result

    
    #assigning different serializer to the special functiosn
    def get_serializer_class(self):
        if self.action=="special_function":
            return SpecialFunctionInputSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return WarehouseModelSerializer2
        return WarehouseModelSerializer1
    


class TemporaryModelViewSet(viewsets.ModelViewSet):
    queryset = TemporaryModel.objects.all()  
    serializer_class = TemporaryModelSerializer 


                    
                    

           


