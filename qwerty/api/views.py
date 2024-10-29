from rest_framework import viewsets
from rest_framework.decorators import action
from django.db.models import Sum
from rest_framework.response import Response


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

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return WarehouseModelSerializer2
        return WarehouseModelSerializer1
    


class TemporaryModelViewSet(viewsets.ModelViewSet):
    queryset=TemporaryModel.objects.all()
    serializer_class=TemporaryModelSerializer



    @action(detail=False, methods=["post"])
    def special_function(self,request):
        new_ones=request.data.get("products")
        res1=[]
        for no in new_ones:
            product=ProductModel.objects.get(id=no["product_id"])
            qw={}
            qw["product_name"]=product.name
            qw["product_qty"]=no["quantity"]
            wq=[]
            needed_materials=ProductMaterialModel.objects.filter(product_id=product)
            print(needed_materials)
            for nm in needed_materials:
                total_needed_materials=no["quantity"]*nm.quantity
                available_materials=WarehouseModel.objects.filter(free__gt=0,material_id=nm.material_id)
                for am in available_materials:
                    min_materials=min(am.free,total_needed_materials)
                    if min_materials<1:
                        break
                    total_needed_materials-=min_materials
                    am.free-=min_materials
                    am.save()
                    zxc={"warehouse_id":am.pk,
                            "material_name":am.material_id.name,
                            "qty":min_materials,
                            "price":am.price}
                    wq.append(zxc)

                if total_needed_materials>0:
                    zxc={"warehouse_id":None,
                            "material_name":nm.material_id.name,
                            "qty":total_needed_materials,
                            "price":None}
                    wq.append(zxc)
                    

            qw["product_materials"]=wq

            res1.append(qw)
        
        return Response({"result":res1})



    def get_serializer_class(self):
        if self.action=="special_function":
            return SpecialFunctionInputSerializer
        return TemporaryModelSerializer
    
                    
                    

           


