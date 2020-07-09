from django.urls import path
from .views import GoodsGroupView, ItemView, SKUView

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('sku', SKUView, basename='sku')
router.register('groups', GoodsGroupView, basename='groups')
router.register('items', ItemView, basename='items')

urlpatterns = router.urls