from django.shortcuts import render
from .models import Item, SKU, GoodsGroup
from rest_framework.viewsets import ModelViewSet
from .serializers import ItemSerializer, ItemUpdateSerializer, GoodsGroupSerializer, SKUSerializer
from .filters import ItemFilter

class SKUView(ModelViewSet):
    queryset = SKU.objects.all()
    serializer_class = SKUSerializer
    filterset_fields = ['name']


class GoodsGroupView(ModelViewSet):
    queryset = GoodsGroup.objects.all()
    serializer_class = GoodsGroupSerializer
    filterset_fields = ['name']


class ItemView(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filterset_class = ItemFilter
    search_fields = ['name']

    def __init__(self, *args, **kwargs):
        super(ItemView, self).__init__(*args, **kwargs)
        self.serializer_action_classes ={
        'create': ItemSerializer,
        'update': ItemUpdateSerializer,
        'partial_update': ItemUpdateSerializer,
        'retrieve': ItemUpdateSerializer
        }

    def get_serializer_class(self, *args, **kwargs):
        """Instantiate the list of serializers per action from class attribute (must be defined)."""
        kwargs['partial'] = True
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(ItemView, self).get_serializer_class()

