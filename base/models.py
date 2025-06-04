from django.db import models

# Expense tracker model

class ExpenseTrackerModel(models.Model):

    TRANSACTION_TYPES = [
        ('expense', 'Expense'),
        ('income', 'Income'),
    ]

    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES, default='expense')
    activity = models.CharField(max_length=50, null=True)
    value = models.DecimalField(decimal_places=2, max_digits=10, blank=True)
    date = models.DateField()

    class Meta:
        ordering = ['-date']

    def __str__(self) -> str:
        sign = "-" if self.transaction_type == "expense" else "+"
        return f"{self.activity} ({sign}${abs(self.value):.2f}) on {self.date}"