from decimal import Decimal

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import F

from .models import *
from .serializers import *


class AllItemsAPIView(APIView):
    def get(self, request):
        items = Items.objects.all()
        serializer = ItemsSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ItemsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemDetailAPIView(APIView):
    def get_object(self, id):
        return get_object_or_404(Items, id=id)

    def get(self, request, id):
        item = self.get_object(id)
        serializer = ItemsSerializer(item)
        return Response(serializer.data)

    def put(self, request, id):
        item = self.get_object(id)
        serializer = ItemsSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        item = self.get_object(id)
        item.delete()
        return Response({'message': 'Item deleted successfully'}, status=status.HTTP_200_OK)


class CartAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user)
        # Use CartSerializer for consistent response
        serializer = CartSerializer(cart, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        slug = request.data.get('slug')
        try:
            quantity = int(request.data.get('quantity', 1))
        except (TypeError, ValueError):
            return Response({'error': 'quantity must be an integer'}, status=status.HTTP_400_BAD_REQUEST)

        if not slug:
            return Response({'error': 'slug is required'}, status=status.HTTP_400_BAD_REQUEST)

        item = get_object_or_404(Items, slug=slug)
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item, defaults={'quantity': quantity})
        if not created:
            cart_item.quantity = F('quantity') + quantity
            cart_item.save()
            cart_item.refresh_from_db()

        serializer = CartSerializer(cart, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        slug = request.data.get('slug')
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user)

        if slug:
            item = get_object_or_404(Items, slug=slug)
            cart_item = CartItem.objects.filter(cart=cart, item=item).first()
            if not cart_item:
                return Response({'error': 'item not in cart'}, status=status.HTTP_404_NOT_FOUND)
            cart_item.delete()
            serializer = CartSerializer(cart, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        # clear whole cart
        cart.cart_items.all().delete()
        serializer = CartSerializer(cart, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)



