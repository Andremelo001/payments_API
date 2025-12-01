class QrCodeGenerationError(Exception):
    
    def __init__(self, message: str, schedule_id: str = None):
        super().__init__(message)
        self.message = f"Failed to generate QR Code: {message}"
        self.name = 'QrCodeGenerationError'
        self.status_code = 500
        self.schedule_id = schedule_id
