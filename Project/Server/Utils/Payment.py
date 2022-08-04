from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from Server.Database import Razorpay_collection,Stripe_collection
from Server.Models.Payment import Payment_id, Get_Payment_Status
import razorpay
from datetime import datetime, timedelta

from bson.objectid import ObjectId
import stripe


router = APIRouter()

razorpay_key_id = 'rzp_test_w1LsgSW71gCHBV'
razorpay_key_secret = 'JQTEBUBvXGExFG1riOmsQQCg'
client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))

stripe_keys = {
    "secret_key": "sk_test_51L65Q8SAICnMJG787DkXEk5D3B9Ast0fSWaqBYqRWfZ3ubmVO5kshuHC0ay50iGqVdCgEgzfRfRtoKAuPpK2yhFs00O87zW2SR",
    "publishable_key": "pk_test_51L65Q8SAICnMJG789W3a7vj2B2hD0Oq5Pqk6RkhXkhgl7MCdpLxx0raz6esebaXJd4WvOoXJdusqE9EsYS5bn5lE00lP0KiBt5",
    # "endpoint_secret": "whsec_e7bf288f56ee8532d216de20904360e1762f1144f55ec5a0b0dc3e95b9f9c8cb"
}
stripe.api_key = stripe_keys["secret_key"]


def Payment_helper(order, pays, id, MODE) -> dict:
    return {
            "Uid": id,
            "PRICE": pays['amount'],
            "Duration": pays['notes']['DURATION'],
            "TYPE": pays['notes']['Name'],
            "STATUS": "PENDING",
            "PAYMENT_ID": order['id'],
            "SOURCE": MODE,
            }


def Mode_helper(Payments, day) -> dict:
    return{
        "START_AT": str(datetime.now()),
        "STATUS": Payments,
        "EXPIRY_AT": str(datetime.now() + timedelta(days=day))
    }

def stripe_helper(session,id) -> dict:
    return  {
                "Uid":id,
                "PRICE": session['amount_total'],
                "Duration": "3 Months",
                "TYPE": "Card",
                "STATUS": session["payment_status"],
                "PAYMENT_ID": session['id'],
                "PAYMENT_INTENT": session["payment_intent"],
                "SOURCE": "Stripe",
                "URL":session['url'],
                "url_status":session['status'],
            }      

def Mode_helper(Payments,day) ->dict:
    return{
                    "START_AT": str(datetime.now()),
                    "STATUS": Payments, 
                    "EXPIRY_AT": str(datetime.now() + timedelta(days=day))
    }


@router.post('/razorpay/{id}', response_description="Payment request")
async def pay(id: str, pays: Payment_id = Body(...)):
    pays = jsonable_encoder(pays)
    User = await Razorpay_collection.find_one({"Uid": id})
    if User:
        if User['STATUS'] == "PENDING":
            return {"PAYMENT_ID": User['PAYMENT_ID'], "STATUS": User['STATUS'], "PRICE": User['PRICE'], "SOURCE": User['SOURCE'], 'User_id': User['Uid'], 'key_id': razorpay_key_id}
        else:
            return {"Msg": "Payment already done"}
    order = client.order.create(data=pays)
    await Razorpay_collection.insert_one(Payment_helper(order, pays, id, "RAZORPAY"))
    return {"data": order, "status": "success", "Data": "User_Payment", 'key_id': razorpay_key_id}


@router.post('/razorpay_Payment/{id}', response_description="Payment status")
async def status(id: str, day: int, data: Get_Payment_Status = Body(...)):
    data = jsonable_encoder(data)
    try:
        Payments = client.utility.verify_payment_signature(data)
        datas = Mode_helper(Payments, day)
        
        await Razorpay_collection.update_one(
            {"Uid":  id}, {'$set': datas})
        return {"Payments": 'success', "status": Payments}
    except:
        Payments = False

        return {"Payments": 'Failed',"status": Payments}


@router.post("/stripe-create-checkout-session/{id}")
async def create_checkout_session(id: str):
    domain_url = "http://localhost:8000/"
    stripe.api_key = stripe_keys["secret_key"]
    User= await Stripe_collection.find_one({"Uid":id})
    # print(User)
    if User:
        if User['STATUS']=="unpaid":
            if User['url_status']=="open":
              return {"PAYMENT_ID":User['PAYMENT_ID'],"STATUS":User['STATUS'],"PRICE":User['PRICE'],"SOURCE":User['SOURCE'],'User_id':User['Uid'],'payment_url':User['URL']}
        else:
            return {"Msg":"Payment already captured"}
    else:   
        try:
            session = stripe.checkout.Session.create(
                success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "cancelled",
                line_items=[
                    {
                    "price": "price_1L65vvSAICnMJG78OjFRsHb0",
                    "quantity": 1,
                    },
                ],
                mode="payment",
            )          
            await Stripe_collection.insert_one(stripe_helper(session,id))
            return session["url"],session["status"]
        except Exception as e:
            return e

@router.post('/stripe_Payment/{id}', response_description="Payment status")
async def status(userid: str,day:int,payment_session_id:str):
    stripe.api_key = stripe_keys["secret_key"]
    try:
        session = stripe.checkout.Session.retrieve(
            payment_session_id,
            )
        if session["payment_status"]=="paid":
            datas= Mode_helper("paid",day)
            await Stripe_collection.update_one(
                {"Uid":  userid}, {'$set': datas })
            await Stripe_collection.update_one(
                {"Uid":  userid}, {'$set': { "url_status": "complete" } })
            return {"Payments": 'success', "status": True}
        else:
            return {"Payments": 'Pending Payment',"status": False}
            
    except:
        return {"Payments": 'Failed',"status": False}
