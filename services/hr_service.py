class HRService:
    """
    Mock external HR system (authoritative dynamic data source)
    """

    def get_remaining_vacation_days(self, user_id: str) -> int:
        return 12
