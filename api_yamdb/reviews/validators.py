from datetime import datetime
from django.core.exceptions import ValidationError


def validate_year(value):
    current_date = datetime.now().year
    if value > current_date:
        raise ValidationError(
            f'Выберете уже прошедший год - нельзя указать {current_date}'
        )
