class NotificationError(Exception):
    
    def __init__(self, schedule_id: str, status: str, reason: str = "Unknown error"):
        super().__init__(f"Failed to notify main API for schedule_id: {schedule_id}")
        self.message = f"Failed to notify main API for schedule_id: {schedule_id}. Reason: {reason}"
        self.name = 'NotificationError'
        self.status_code = 500
        self.schedule_id = schedule_id
        self.status = status
        self.reason = reason
