from src.main.api.models.base_model import BaseModel

class RepayCreditResponse(BaseModel):
    credit_id: int
    amountDeposited: float