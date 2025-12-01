class ValidationError(Exception):
    
    def __init__(self, message: str, field: str = None):
        super().__init__(message)
        self.message = message
        self.name = 'ValidationError'
        self.status_code = 422
        self.field = field
