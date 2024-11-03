from datetime import datetime, timedelta

class DateUtils:
    @staticmethod
    def get_current_timestamp() -> str:
        """Get the current timestamp in ISO format."""
        return datetime.utcnow().isoformat()

    @staticmethod
    def add_days_to_date(date: datetime, days: int) -> datetime:
        """Add days to a given date."""
        return date + timedelta(days=days)

# Example usage
if __name__ == "__main__":
    current_time = DateUtils.get_current_timestamp()
    future_date = DateUtils.add_days_to_date(datetime.utcnow(), 10)

    print(f"Current Timestamp: {current_time}")
    print(f"Future Date: {future_date.isoformat()}")
