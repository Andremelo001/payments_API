class MercadoPagoPaymentNotFoundError(Exception):
    
    def __init__(self, payment_id: str):
        super().__init__(f"Payment not found in Mercado Pago with id: {payment_id}")
        self.message = f"Payment not found in Mercado Pago with id: {payment_id}"
        self.name = 'MercadoPagoPaymentNotFound'
        self.status_code = 404
        self.payment_id = payment_id
