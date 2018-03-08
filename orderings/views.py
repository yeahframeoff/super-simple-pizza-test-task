from django.shortcuts import render
from rest_framework import viewsets, mixins
from .models import Order
from .serializers import OrderSerializer


class PizzaOrderViewSet(mixins.CreateModelMixin,
	                    mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
