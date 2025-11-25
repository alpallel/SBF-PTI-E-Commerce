from decimal import Decimal

from django.test import TestCase

from .models import User, Category, Items, Cart, CartItem
from .serializers import CartSerializer


class CartSerializerTest(TestCase):
	def test_cart_serializer_total(self):
		user = User.objects.create(username='alice', user_password='pass')
		cat = Category.objects.create(name='Cat', slug='cat')
		item1 = Items.objects.create(item_name='Item1', item_category=cat, price=Decimal('10.00'), slug='item-1')
		item2 = Items.objects.create(item_name='Item2', item_category=cat, price=Decimal('5.50'), slug='item-2')
		cart = Cart.objects.create(user=user)
		CartItem.objects.create(cart=cart, item=item1, quantity=2)  # 20.00
		CartItem.objects.create(cart=cart, item=item2, quantity=1)  # 5.50

		serializer = CartSerializer(cart, context={'request': None})
		data = serializer.data
		self.assertIn('total_price', data)
		# total should be 20.00 + 5.50 = 25.50
		self.assertEqual(data['total_price'], '25.50')

