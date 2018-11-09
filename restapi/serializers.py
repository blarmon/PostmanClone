from rest_framework import serializers
from PostmanClone.models import Collection, apiCall

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ("user", "name")
