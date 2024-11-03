import re

class ValidationUtils:
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email address format."""
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    @staticmethod
    def is_valid_transaction_amount(amount: float) -> bool:
        """Validate transaction amount."""
        return amount > 0

# Example usage
if __name__ == "__main__":
    email = "test@example.com"
    amount = 100.0

    print(f"Is valid email: {ValidationUtils.is_valid_email(email)}")
    print(f"Is valid amount: {ValidationUtils.is_valid_transaction_amount(amount)}")
