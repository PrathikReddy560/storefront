from django.test import TestCase
from uuid import uuid4

from store.serializer import AddCartItemSerializer


class AddCartItemSerializerTests(TestCase):
    def test_product_id_zero_is_rejected_during_validation(self):
        serializer = AddCartItemSerializer(
            data={'product_id': 0, 'quantity': 1},
            context={'cart_id': uuid4()},
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('product_id', serializer.errors)
