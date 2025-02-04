from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Currency(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name=_("Currency Code"))
    name = models.CharField(max_length=50, verbose_name=_("Currency Name"), unique=True)
    decimal_places = models.PositiveIntegerField(
        default=2,
        validators=[MaxValueValidator(30), MinValueValidator(0)],
        verbose_name=_("Decimal Places"),
    )
    prefix = models.CharField(max_length=10, verbose_name=_("Prefix"), blank=True)
    suffix = models.CharField(max_length=10, verbose_name=_("Suffix"), blank=True)

    exchange_currency = models.ForeignKey(
        "self",
        verbose_name=_("Exchange Currency"),
        on_delete=models.SET_NULL,
        related_name="exchange_currencies",
        null=True,
        blank=True,
        help_text=_("Default currency for exchange calculations"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")

    def clean(self):
        super().clean()
        if self.exchange_currency == self:
            raise ValidationError(
                {
                    "exchange_currency": _(
                        "Currency cannot have itself as exchange currency."
                    )
                }
            )


class ExchangeRate(models.Model):
    from_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="from_exchange_rates",
        verbose_name=_("From Currency"),
    )
    to_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="to_exchange_rates",
        verbose_name=_("To Currency"),
    )
    rate = models.DecimalField(
        max_digits=42, decimal_places=30, verbose_name=_("Exchange Rate")
    )
    date = models.DateTimeField(verbose_name=_("Date and Time"))

    class Meta:
        verbose_name = _("Exchange Rate")
        verbose_name_plural = _("Exchange Rates")
        unique_together = ("from_currency", "to_currency", "date")

    def __str__(self):
        return f"{self.from_currency.code} to {self.to_currency.code} on {self.date}"

    def clean(self):
        super().clean()
        # Check if the attributes exist before comparing them
        if hasattr(self, "from_currency") and hasattr(self, "to_currency"):
            if self.from_currency == self.to_currency:
                raise ValidationError(
                    {"to_currency": _("From and To currencies cannot be the same.")}
                )
