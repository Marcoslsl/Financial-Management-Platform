from django.db import models
from django.utils import timezone


class Purchase(models.Model):
    EDUCATION = "Education"
    HEALTH = "Health"
    TRAVEL = "Travel"
    ELECTRONICS = "Electronics"
    INVESTMENT = "Investment"
    CLOTHING = "Clothing"
    FOOD = "Food"
    ENTERTAINMENT = "Entertainment"
    HOME = "HOME"

    YES = "Yes"
    NO = "No"

    CATEGORY_CHOICES = [
        (EDUCATION, "Education"),
        (HEALTH, "Health"),
        (TRAVEL, "Travel"),
        (ELECTRONICS, "Electronics"),
        (INVESTMENT, "Investment"),
        (CLOTHING, "Clothing"),
        (FOOD, "Food"),
        (ENTERTAINMENT, "Entertainment"),
        (HOME, "Home"),
    ]

    CREDIT_CARD_CHOICES = [(YES, "sim"), (NO, "Não")]

    name = models.CharField(max_length=30)
    price = models.PositiveIntegerField(default=0)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default=None
    )
    credit_card = models.CharField(max_length=12, choices=CREDIT_CARD_CHOICES)
    day_to_receive_the_analysis = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=250)
    data_of_purchase = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
