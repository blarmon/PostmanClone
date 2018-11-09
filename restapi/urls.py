from django.urls import path
from .views import ListCollectionView

urlpatterns = [
    path('collections/', ListCollectionView.as_view(), name="collections-all")
]