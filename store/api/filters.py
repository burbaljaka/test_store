from django_filters import rest_framework as filters
from .models import Item, GoodsGroup, SKU

class ItemFilter(filters.FilterSet):
    sku = filters.CharFilter(field_name='sku__name', lookup_expr='icontains')
    group = filters.CharFilter(field_name='group__name', lookup_expr='icontains')
    less_last = filters.NumberFilter(field_name='quantity', lookup_expr='lte')
    more_last = filters.NumberFilter(field_name='quantity', lookup_expr='gte')
    less_res = filters.NumberFilter(field_name='reserved', lookup_expr='lte')
    more_res = filters.NumberFilter(field_name='reserved', lookup_expr='gte')

    class Meta:
        model = Item
        fields = ['sku', 'group', 'less_last', 'more_last', 'less_res', 'more_res']