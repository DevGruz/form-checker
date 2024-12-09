import re
from datetime import datetime


class FormFieldValidator:

    @staticmethod
    def validate(value: str) -> str:
        if FormFieldValidator.is_email(value):
            return "email"
        if FormFieldValidator.is_phone(value):
            return "phone"
        if FormFieldValidator.is_date(value):
            return "date"
        return "text"

    @staticmethod
    def is_email(value: str) -> bool:
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.match(email_regex, value))

    @staticmethod
    def is_phone(value: str) -> bool:
        phone_regex = r"^\+7 \d{3} \d{3} \d{2} \d{2}$"
        return bool(re.match(phone_regex, value))

    @staticmethod
    def is_date(value: str) -> bool:
        date_formats = ["%d.%m.%Y", "%Y-%m-%d"]
        for fmt in date_formats:
            try:
                datetime.strptime(value, fmt)
                return True
            except ValueError:
                continue
        return False
