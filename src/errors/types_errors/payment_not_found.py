class PaymentNotFoundError(Exception):
    
    def __init__(self, identifier: str, identifier_type: str = "schedule_id"):
        super().__init__(f"Payment not found for {identifier_type}: {identifier}")
        self.message = f"Payment not found for {identifier_type}: {identifier}"
        self.name = 'PaymentNotFound'
        self.status_code = 404
        self.identifier = identifier
        self.identifier_type = identifier_type
