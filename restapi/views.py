from django.shortcuts import render
from rest_framework import generics
from PostmanClone.models import Collection, apiCall
from .serializers import CollectionSerializer, ApiCallSerializer
import ast

class ListCollectionView(generics.ListAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def get_queryset(self):
        user = self.request.user
        return Collection.objects.filter(user=user)

class ListCallView(generics.ListAPIView):
    queryset = apiCall.objects.all()
    serializer_class = ApiCallSerializer

    def get_queryset(self):
        user = self.request.user
        my_collection_queryset = Collection.objects.filter(user=user)
        return apiCall.objects.filter(collection__in=my_collection_queryset)

class CreateCollectionView(generics.CreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

class CreateCallView(generics.CreateAPIView):
    queryset = apiCall.objects.all()
    serializer_class = ApiCallSerializer
