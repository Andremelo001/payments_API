class PaymentAlreadyExistsError(Exception):
    
    def __init__(self, schedule_id: str):
        super().__init__(f"Payment already exists for schedule_id: {schedule_id}")
        self.message = f"Payment already exists for schedule_id: {schedule_id}"
        self.name = 'PaymentAlreadyExists'
        self.status_code = 409
        self.schedule_id = schedule_id
