import json
from users.models import Purchase
from django.http import HttpRequest, JsonResponse


class Analise:
    def __init__(self) -> None:
        self.__purchase = Purchase

    def return_json_purchase(self, request: HttpRequest) -> dict:
        purchases = self.__purchase.objects.filter(user=request.user)
        purchases_list = [
            {
                "name": purchase.name,
                "price": purchase.price,
                "category": purchase.category,
                "credit_card": purchase.credit_card,
                "description": purchase.description,
                "data_of_purchase": purchase.data_of_purchase,
            }
            for purchase in purchases
        ]
        return purchases_list
