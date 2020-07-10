from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from .models import Item, GoodsGroup, SKU
from django.urls import reverse
from rest_framework import status

class ItemTestCases(APITestCase):
    @classmethod
    def setUpClass(cls):
        # cls.cls_atomic = cls._enter_atomics()
        cls.sku = SKU.objects.create(name='shoes')
        cls.group = GoodsGroup.objects.create(name='sport')
        cls.item = Item.objects.create(name='Sneakers Nike',
                                       sku=cls.sku,
                                       group=cls.group)

        cls.item_with_quantity = Item.objects.create(name='Flippers',
                                                    sku=cls.sku,
                                                    group=cls.group,
                                                    quantity=40)

        cls.item_with_quantity_and_reserve = Item.objects.create(name='Slates',
                                                                sku=cls.sku,
                                                                group=cls.group,
                                                                quantity=50,
                                                                reserved=30)
        cls.item_with_reserve = Item.objects.create(name='Boots',
                                                    sku=cls.sku,
                                                    group=cls.group,
                                                    reserved=30)


    def test_default_data(self):
        self.assertEqual(self.item.quantity, 0.0)
        self.assertEqual(self.item.reserved, 0.0)

    def test_sku_creation(self):
        data = {'name': 'hats'}
        response = self.client.post(reverse('sku-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])

    def test_group_creation(self):
        data = {'name': 'party'}
        response = self.client.post(reverse('groups-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['id'], 2)

    def test_item_creation_with_existing_sku_and_group_fail(self):
        data = {'name': 'testItem',
                'quantity': 'abc',
                'sku_name': self.sku.name,
                'group_name': self.group.name}
        response = self.client.post(reverse('items-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_item_creation_with_existing_sku_and_group_success(self):
        data = {'name': 'testItem',
                'quantity': 50,
                'sku_name': self.sku.name,
                'group_name': self.group.name}
        response = self.client.post(reverse('items-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['quantity'], float(data['quantity']))
        self.assertEqual(response.data['reserved'], 0.0)
        self.assertEqual(response.data['sku']['name'], self.sku.name)
        self.assertEqual(response.data['sku']['id'], self.sku.id)
        self.assertEqual(response.data['group']['id'], self.group.id)
        self.assertEqual(response.data['group']['name'], self.group.name)

    def test_item_creation_with_new_sku_and_group(self):
        data = {'name': 'testItem',
                'quantity': 50,
                'sku_name': 'weapon',
                'group_name': 'miniguns'}
        response = self.client.post(reverse('items-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['quantity'], float(data['quantity']))
        self.assertEqual(response.data['reserved'], 0.0)
        self.assertEqual(response.data['sku']['name'], data['sku_name'])
        self.assertEqual(response.data['group']['name'], data['group_name'])

        sku_last = SKU.objects.last()
        group_last = GoodsGroup.objects.last()

        self.assertEqual(response.data['sku']['id'], sku_last.id)
        self.assertEqual(response.data['group']['id'], group_last.id)

    def test_change_quantity_item_operation_name_fail(self):
        data = {'number': 20, 'operation': 'Incorrect_name'}
        response = self.client.patch(reverse('items-detail', kwargs={'pk': self.item.id}),
                                     data=data,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.item.quantity, 0.0)

    def test_addition_item_operation_fail(self):
        data = {'number': -20, 'operation': 'addition'}
        response = self.client.patch(reverse('items-detail', kwargs={'pk': self.item.id}),
                                     data=data,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.item.quantity, 0.0)
        self.assertEqual(self.item.reserved, 0.0)

    def test_addition_item_success(self):
        data = {'number': 20, 'operation': 'addition'}
        response = self.client.patch(reverse('items-detail', kwargs={'pk': self.item.id}),
                                     data=data,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 20.0)
        self.assertEqual(response.data['reserved'], 0.0)

    def test_sell_item_fail(self):
        data = {'number': 30, 'operation': 'sell'}
        response = self.client.patch(reverse('items-detail', kwargs={'pk': self.item.id}),
                                     data=data,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.item.quantity, 0.0)
        self.assertEqual(self.item.reserved, 0.0)

    def test_sell_item_success(self):
        data = {'number': 20, 'operation': 'sell'}
        response = self.client.patch(reverse('items-detail',
                                             kwargs={'pk': self.item_with_quantity.id}),
                                     data=data,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 20.0)
        self.assertEqual(response.data['reserved'], 0.0)

    def test_sell_from_reserve_fail(self):
        data = {'number': 30, 'operation': 'sell_reserve'}
        response = self.client.patch(reverse('items-detail', kwargs={'pk': self.item.id}),
                                     data=data,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.item.quantity, 0.0)
        self.assertEqual(self.item.reserved, 0.0)

    def test_sell_from_reserve_success(self):
        data = {'number': 20, 'operation': 'sell_reserve'}
        response = self.client.patch(reverse('items-detail',
                                             kwargs={'pk': self.item_with_reserve.id}),
                                     data=data,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 0.0)
        self.assertEqual(response.data['reserved'], 10.0)

    def test_reserve_fail(self):
        data = {'number': 30, 'operation': 'reserve'}
        response = self.client.patch(reverse('items-detail', kwargs={'pk': self.item.id}),
                                     data=data,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.item.quantity, 0.0)
        self.assertEqual(self.item.reserved, 0.0)

    def test_reserve_success(self):
        data = {'number': 20, 'operation': 'reserve'}
        response = self.client.patch(reverse('items-detail',
                                             kwargs={'pk': self.item_with_quantity.id}),
                                     data=data,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 20.0)
        self.assertEqual(response.data['reserved'], 20.0)

    def test_remove_from_reserve_fail(self):
        data = {'number': 30, 'operation': 'remove_reserve'}
        response = self.client.patch(reverse('items-detail', kwargs={'pk': self.item.id}),
                                     data=data,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.item.quantity, 0.0)
        self.assertEqual(self.item.reserved, 0.0)

    def test_reserve_success(self):
        data = {'number': 20, 'operation': 'remove_reserve'}
        response = self.client.patch(reverse('items-detail',
                                             kwargs={'pk': self.item_with_reserve.id}),
                                     data=data,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 20.0)
        self.assertEqual(response.data['reserved'], 10.0)

    @classmethod
    def tearDownClass(cls):
        pass
