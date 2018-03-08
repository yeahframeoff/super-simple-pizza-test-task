from django.test import TestCase
from django.forms.models import model_to_dict
from rest_framework.test import APIClient
from .models import Pizza, Order


class OrdersTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.margherita =\
            Pizza.objects.create(name="Margherita",
                                 description="Mozarella, basil, tomatoes, olive oil")

        self.quattro_formaggi =\
            Pizza.objects.create(name="Quattro Formaggi",
                                 description="Red onion, saga blue, gruyere, mozarella, parmesan")

    def test_create_order(self):
        order_json = {
            'pizza': self.margherita.id,
            'size': '30',
            'customer_name': 'John Doe',
            'customer_address': 'Hauptstrasse 16, 12345, Muensterdort',
        }

        self.client.post('/orders/', order_json, format='json')

        order = Order.objects.filter()[0]
        model_data = model_to_dict(order)
        del model_data['id']   # no need to check id
        self.assertDictEqual(order_json, model_data)

    def test_remove_order(self):
        order_data = {
            'pizza': self.margherita,
            'size': '30',
            'customer_name': 'John Doe',
            'customer_address': 'Hauptstrasse 16, 12345, Muensterdort',
        }
        order = Order.objects.create(**order_data)

        self.assertEqual(Order.objects.count(), 1)

        self.client.delete('/orders/{}/'.format(order.id))

        self.assertEqual(Order.objects.count(), 0)
    
    def test_update_order(self):
        order_data = {
            'pizza': self.margherita,
            'size': '30',
            'customer_name': 'John Doe',
            'customer_address': 'Hauptstrasse 16, 12345, Muensterdort',
        }
        order = Order.objects.create(**order_data)

        updated_order_json = {
            'pizza': self.quattro_formaggi.id,
            'size': '30',
            'customer_name': 'John Doe',
            'customer_address': 'Hauptstrasse 16, 12345, Muensterdort',
        }

        self.client.put('/orders/{}/'.format(order.id), updated_order_json, format='json')

        order = Order.objects.filter()[0]
        model_data = model_to_dict(order)
        del model_data['id']   # no need to check id
        self.assertDictEqual(updated_order_json, model_data)

    def test_list_orders(self):
        orders_data = [{
            'pizza': self.margherita,
            'size': '30',
            'customer_name': 'John Doe',
            'customer_address': 'Hauptstrasse 16, 12345, Muensterdort',
        }, {
            'pizza': self.quattro_formaggi,
            'size': '50',
            'customer_name': 'Dave Smith',
            'customer_address': 'Westring 22, 54321, Schnabelwaid',
        }, ]

        order = Order.objects.bulk_create(Order(**data) for data in orders_data)

        resp = self.client.get('/orders/')

        resp_json = resp.json()

        # normalizing data before compare

        for item in resp_json:
            del item['id']

        for item in orders_data:
        	item['pizza'] = item['pizza'].id

        self.assertListEqual(resp_json, orders_data)

    