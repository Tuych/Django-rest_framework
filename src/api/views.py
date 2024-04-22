from django.shortcuts import render
from django.http import JsonResponse
from .models import Product
from .serializers import ProductSerializers
from django.forms.models import model_to_dict

from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def api_main(request, *args, **kwargs):
    model_data = Product.objects.all().first()
    # data = {}

    # data['id'] = model_data.id
    # data['description'] = model_data.description
    # data['price'] = model_data.price
    # data = model_to_dict(model_data)

    data = ProductSerializers(model_data).data
    

    return Response(data)
