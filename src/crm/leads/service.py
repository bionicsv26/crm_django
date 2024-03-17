from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class UnicodeNameValidator(validators.RegexValidator):
    """Класс валидатора имени."""

    regex = r"^[А-ЯЁа-яёA-Za-z\s]+\Z"
    message = "Enter a valid name. This value may contain only letters and whitespace "
    flags = 0


@deconstructible
class UnicodeNumberValidator(validators.RegexValidator):
    """Класс валидатора номера телефона."""

    regex = r"^\+?\d{1,3}\d{10}"
    message = "Enter a valid number. The number must consist of a region code and 10 digits "
    flags = 0
