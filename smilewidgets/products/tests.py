from rest_framework import status
from rest_framework.test import APITestCase

from products.models import ProductPrice
from products.utils import get_formatted_price


class GetPriceTests(APITestCase):
    fixtures = ['0001_fixtures.json']
    url = '/api/get-price'

    # Validation errors
    def validation_error_test(self, field, message, data):
        response = self.client.get(self.url, data, format='json')
        json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(field, json)
        error_message = json[field].pop()
        self.assertEqual(error_message, message)

    def test_empty_product_code(self):
        self.validation_error_test('productCode', 'This field is required.', {'date': '2019-01-01'})

    def test_wrong_product_code(self):
        self.validation_error_test(
            'productCode', 'Product with this code does not exist.', {
                'productCode': 'widget',
                'date': '2019-01-01'
            })

    def test_empty_date(self):
        self.validation_error_test('date', 'This field is required.', {'productCode': 'big_widget'})

    def test_wrong_date(self):
        self.validation_error_test(
            'date', 'Date has wrong format. Use one of these formats instead: YYYY-MM-DD.', {
                'productCode': 'big_widget',
                'date': '01-01-2019',
            })

    def test_wrong_gift_card_code(self):
        self.validation_error_test(
            'giftCardCode', 'Gift card with this code does not exist.', {
                'productCode': 'big_widget',
                'date': '2019-01-01',
                'giftCardCode': 'giftCode',
            })

    # Price calculations. Date
    def price_test(self, expected_price, data):
        response = self.client.get(self.url, data, format='json')
        json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('price', json)
        self.assertEqual(json['price'], get_formatted_price(expected_price))

    def test_before_2019_price(self):
        for widget, expected_price in {'big_widget': 100000, 'sm_widget': 9900}.items():
            for date in ('2018-12-31', '2018-01-01', '2010-01-01'):
                self.price_test(expected_price, {
                    'date': date,
                    'productCode': widget,
                })

    def test_2019_price(self):
        for widget, expected_price in {'big_widget': 120000, 'sm_widget': 12500}.items():
            for date in ('2019-12-31', '2019-01-01', '2030-01-01'):
                self.price_test(expected_price, {
                    'date': date,
                    'productCode': widget,
                })

    def test_black_friday_price(self):
        for widget, expected_price in {'big_widget': 80000, 'sm_widget': 0}.items():
            for date in ('2019-11-23', '2019-11-24', '2019-11-25'):
                self.price_test(expected_price, {
                    'date': date,
                    'productCode': widget,
                })

    # Price calculations. Gift card
    def test_gift_card_exceed_price(self):
        self.price_test(0, {
            'date': '2019-01-01',
            'giftCardCode': '250OFF',
            'productCode': 'sm_widget',
        })

    def test_gift_card_reduced_price(self):
        expected_price = 120000 - 25000
        self.price_test(expected_price, {
            'date': '2019-01-01',
            'giftCardCode': '250OFF',
            'productCode': 'big_widget',
        })

    # Price calculations. Lowest
    def test_gift_card_choose_lowest(self):
        ProductPrice.objects.create(price=200, product_id=2, date_start='2020-01-01')
        lowest_product_price = ProductPrice.objects.create(price=100, product_id=2, date_start='2020-01-01')
        ProductPrice.objects.create(price=300, product_id=2, date_start='2020-01-01')

        self.price_test(lowest_product_price.price, {
            'date': '2020-01-01',
            'productCode': 'sm_widget',
        })
