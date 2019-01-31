from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from products.models import Product, GiftCard


class GetPriceSerializer(serializers.Serializer):
    product_code = serializers.CharField(max_length=10)
    date = serializers.DateField(format=None)
    gift_card_code = serializers.CharField(max_length=30, required=False)

    def validate_product_code(self, code):
        try:
            return Product.objects.get(code=code)
        except Product.DoesNotExist:
            raise ValidationError('Product with this code does not exist.')

    def validate(self, attrs):
        gift_card_code = attrs.get('gift_card_code')
        date = attrs.get('date')

        if gift_card_code is not None:
            try:
                attrs['gift_card_code'] = GiftCard.objects.for_date(date).get(code=gift_card_code)
            except GiftCard.DoesNotExist:
                raise serializers.ValidationError({'gift_card_code': 'Gift card with this code does not exist.'})

        return attrs

