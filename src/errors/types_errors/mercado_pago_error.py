class MercadoPagoError(Exception):
    
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = f"Mercado Pago API Error: {message}"
        self.name = 'MercadoPagoError'
        self.status_code = status_code
