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

    CATEGORY_CHOICES = [
        (EDUCATION, "Education"),
        (HEALTH, "Health"),
        (TRAVEL, "Travel"),
        (ELECTRONICS, "Electronics"),
        (INVESTMENT, "Investment"),
        (CLOTHING, "Clothing"),
        (FOOD, "Food"),
        (ENTERTAINMENT, "Entertainment"),
    ]

    name = models.CharField(max_length=30)
    price = models.PositiveIntegerField(default=0)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default=None
    )
    credit_card = models.BooleanField(default=False)
    day_to_receive_the_analysis = models.DateField(default=timezone.now)
    description = models.CharField(max_length=250)
    data_of_purchase = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField()

    def __str__(self) -> str:
        return self.name
