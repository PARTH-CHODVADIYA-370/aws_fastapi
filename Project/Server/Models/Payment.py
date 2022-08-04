from pydantic import BaseModel


class Payment_id(BaseModel):
    amount: int
    currency: str
    receipt: str
    notes: dict

    class Config:
        schema_extra = {
            "example": {
                "amount": 999 * 999,
                "currency": "INR",
                "receipt": "receipt",
                "notes": {
                    "App_Name": "My_fiti",
                    "Name": "Normal",
                    "DURATION": "3 MONTHS",
                },
            }
        }


class Get_Payment_Status(BaseModel):
    razorpay_payment_id: str
    razorpay_order_id: str
    razorpay_signature: str

    class Config:
        schema_extra = {
            "example": {
                "razorpay_payment_id": "pay_JcAb4u75KW8BDC",
                "razorpay_order_id": "order_Jc8yzeFy5qbJQe",
                "razorpay_signature": "a5c9f74363dca4f935df94c249d7fc4018f965b6c4466e6a9849d18b0674281c",
            }
        }
