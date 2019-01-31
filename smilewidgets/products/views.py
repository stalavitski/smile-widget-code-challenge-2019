from djangorestframework_camel_case.util import underscoreize
from rest_framework.response import Response
from rest_framework.views import APIView

from products.serializers import GetPriceSerializer
from products.utils import get_formatted_price


class GetPriceView(APIView):

    def get(self, request):
        data = underscoreize(data=request.query_params)
        serializer = GetPriceSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data.get('product_code')
        price = product.get_total(
            serializer.validated_data.get('date'),
            serializer.validated_data.get('gift_card_code')
        )
        return Response({
            'price': get_formatted_price(price)
        })
