from src.main.api.models.base_model import BaseModel

class RequestCreditResponse(BaseModel):
    account_id: int
    amount: float
    termMonths: int
    balance: float
    creditId: int