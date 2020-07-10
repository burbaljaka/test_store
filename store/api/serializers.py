from rest_framework import serializers
from .models import Item, SKU, GoodsGroup
from django.db import transaction


class SKUSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = ['id', 'name']


class GoodsGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsGroup
        fields = ['id', 'name']


class ItemSerializer(serializers.ModelSerializer):
    sku = SKUSerializer(read_only=True)
    group = GoodsGroupSerializer(read_only=True)
    sku_name = serializers.CharField(write_only=True)
    group_name = serializers.CharField(write_only=True)

    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ['reserved']

    def create(self, validated_data):
        sku_name = validated_data.pop('sku_name')
        group_name = validated_data.pop('group_name')
        item = super(ItemSerializer, self).create(validated_data)

        sku_list = SKU.objects.filter(name=sku_name).count()
        if sku_list > 0:
            sku = SKU.objects.get(name=sku_name) # if there is SKU with that name, we use it
        else:
            sku = SKU.objects.create(name=sku_name) #otherwise we create a new one
        item.sku = sku


        group_list = GoodsGroup.objects.filter(name=group_name).count()
        if group_list > 0:
            group = GoodsGroup.objects.get(name=group_name)
        else:
            group = GoodsGroup.objects.create(name=group_name)
        item.group = group

        item.save()
        return item

class ItemUpdateSerializer(serializers.ModelSerializer):
    OPERATION_CHOICES = [
        ('addition', 'Addition'),
        ('sell', 'Sell'),
        ('sell_reserve', 'Sell from reserve'),
        ('reserve', 'Reserve'),
        ('remove_reserve', 'Remove from reserve')
    ]
    number = serializers.FloatField(write_only=True)
    operation = serializers.ChoiceField(choices=OPERATION_CHOICES, write_only=True)
    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ['quantity', 'reserved']

    def update(self, instance, validated_data):
        number = validated_data.pop('number')
        operation = validated_data.pop('operation')
        super(ItemUpdateSerializer, self).update(instance, validated_data)

        operations = {
            'addition': instance.addition,
            'sell': instance.sell,
            'sell_reserve': instance.sell_from_reserve,
            'reserve': instance.reserve,
            'remove_reserve': instance.remove_from_reserve
        }

        result, message = operations[operation](number)
        if message:
            raise serializers.ValidationError(message)

        return result


