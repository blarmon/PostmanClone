from rest_framework import serializers
from PostmanClone.models import Collection, apiCall

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ("id", "user", "name")


class ApiCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = apiCall
        fields = ("id", "collection", "name", "base_url", "headersa1", "headersb1", "headersa2", "headersb2", "headersa3", "headersb3", "httpMethod")