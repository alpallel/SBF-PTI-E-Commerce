from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *

class AllItemsAPIView(APIView):
    def get(self, request):
        items = items.objects.all()
        serializer = ItemsSerializer(items, many=True)

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
