from django.shortcuts import render
from rest_framework import generics
from PostmanClone.models import Collection
from .serializers import CollectionSerializer

class ListCollectionView(generics.ListAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer