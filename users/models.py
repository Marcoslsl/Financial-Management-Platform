from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def validate_min_value_of_decimal_field(value: int | float):
    if value < 0:
        raise ValidationError(
            "Number is less than zero", params={"value": value}
        )


class Purchase(models.Model):
    EDUCATION = "Education"
    HEALTH = "Health"
    TRAVEL = "Travel"
    ELECTRONICS = "Electronics"
    INVESTMENT = "Investment"
    CLOTHING = "Clothing"
    FOOD = "Food"
    ENTERTAINMENT = "Entertainment"
    HOME = "Home"

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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validate_min_value_of_decimal_field],
    )
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default=None
    )
    credit_card = models.CharField(max_length=12, choices=CREDIT_CARD_CHOICES)
    day_to_receive_the_analysis = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=250)
    data_of_purchase = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    def update_purchase(self, **kwargs) -> None:
        if "name" in kwargs:
            self.name = kwargs["name"]
        if "price" in kwargs:
            self.price = kwargs["price"]
        if "category" in kwargs:
            self.category = kwargs["category"]
        if "credit_card" in kwargs:
            self.credit_card = kwargs["credit_card"]
        if "description" in kwargs:
            self.description = kwargs[
                "description"
            ]  # Defina a data de atualização como a data e hora atuais
        self.updated_at = timezone.now()

        # Salve as mudanças no banco de dados
        self.save()
        return None

    def __str__(self) -> str:
        return self.name
