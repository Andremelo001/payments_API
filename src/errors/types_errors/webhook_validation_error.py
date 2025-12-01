class WebhookValidationError(Exception):
    
    def __init__(self, message: str):
        super().__init__(message)
        self.message = f"Webhook validation failed: {message}"
        self.name = 'WebhookValidationError'
        self.status_code = 400
