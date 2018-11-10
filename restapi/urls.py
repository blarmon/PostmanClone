from django.urls import path
from .views import ListCollectionView, ListCallView, CreateCollectionView, CreateCallView

urlpatterns = [
    path('collection/list', ListCollectionView.as_view(), name="collections-user"),
    path('collection/create', CreateCollectionView.as_view(), name="collections-create"),
    path('call/list', ListCallView.as_view(), name="calls-user"),
    path('call/create', CreateCallView.as_view(), name="call-create"),
]