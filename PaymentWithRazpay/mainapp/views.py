# https://razorpay.com/docs/payment-gateway/server-integration/python/

# https://docs.djangoproject.com/en/3.2/ref/csrf/#setting-the-token-on-the-ajax-request

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import razorpay
import json

client = razorpay.Client(auth=("YOUR_ID", "YOUR_SECRET"))


def simple_payment(request):
    amount = 500
    amount_in_paisa = amount*100  # Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paisa (razorpay docs)
    data = {
         "amount": amount, 
         "currency": "INR", 
         "receipt": "I_have_to_create_random_receipt_id" 
    }
    payment = client.order.create(data=data)
    order_id = payment['id']
    return render(request, 'payment_form.html', {'amount':amount, 'order_id':order_id})

def store_and_verify_payment(request):
    param_dict = json.loads(request.body)
    # Store data provided in request.body in the models then verify the payment.
    # param_dict is like this
    param_dict = {
        'razorpay_order_id': param_dict['razorpay_order_id'],
        'razorpay_payment_id': param_dict['razorpay_payment_id'],
        'razorpay_signature': param_dict['razorpay_signature']
    }
    # How I know that if payment signature fails then it will create error?
    # Just go to verify_payment_signature function in razorpay library and there you will find that
    # this function does not return any thing but if razorpay payment signature fails then it creates error.
    try:
        client.utility.verify_payment_signature(param_dict)
    except:
        return JsonResponse({
        'status':'Payment failed'
    })
    else:
        return JsonResponse({
            'status':'Payment Succeed'
        })