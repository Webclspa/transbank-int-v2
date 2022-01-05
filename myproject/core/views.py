from django.shortcuts import render
import requests
from django.views.decorators.csrf import csrf_exempt

import transbank
from transbank.webpay import webpay_plus
from transbank.webpay.webpay_plus import WebpayPlus
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.webpay.webpay_plus.mall_transaction import MallTransaction, MallTransactionCreateDetails
from transbank.webpay.webpay_plus import IntegrationType
from transbank.error.transbank_error import TransbankError
import random
from django.http import HttpResponseRedirect

@csrf_exempt 
def base(request):
    try:
       #UNCOMMENT FOR PRODUCTION
        #webpay_plus.WebpayPlus.webpay_plus_default_commerce_code = str("my_commerce_code")
        #webpay_plus.WebpayPlus.default_api_key = "my_api_key"
        #webpay_plus.default_integration_type = IntegrationType.LIVE
        #WebpayPlus.configure_for_production(webpay_plus.WebpayPlus.webpay_plus_default_commerce_code,webpay_plus.WebpayPlus.default_api_key)
       
        buy_order = str(random.randrange(1000000, 99999999))
        session_id = str(random.randrange(1000000, 99999999))
        amount = random.randrange(100000, 999999)       
        return_url = 'http://127.0.0.1:8000/exito'

        response = Transaction.create(buy_order, session_id, amount, return_url)
    
        token = request.GET.get("token_ws")
        token = response.token
 
   
        
    except TransbankError as e:
        print(e.message)

    
 
    context = {
        'response': response,
      
    }
    
    return render(request, 'base.html', context)
@csrf_exempt 
def success(request):
    try:
        token = request.GET.get("token_ws")
        response = Transaction.commit(token)
        print(token)
        context = { 'response': response}
        print("Token ws this right here --> ",token)
        return render(request, 'success.html', context)
            

    except TransbankError as e:
        print(e.message)
        
    if request.method == "POST":
       token_tbk = request.POST.get("TBK_TOKEN")
       recuest = request.POST
       orden_compra= request.POST.get('TBK_ORDEN_COMPRA')
       id_sesion = request.POST.get('TBK_ID_SESION')
       print("TBK_TOKEN: ", token_tbk)
       print("PROOF")
       print("orden de compra: ", orden_compra)
       print("sesion_id: ", id_sesion)
       context = {
           'token_tbk': token_tbk,

       } 

    
    return render(request, 'success.html', context) 
    
    
    
def refund(request):
    try:

        token = request.GET.get("token_ws")
        amount = 1000
        response = Transaction.refund(token, amount)
        # token = request.GET.get("TOKEN_TBK")
        # amount = random.randrange(100000, 999999)
        # response = Transaction.refund(token, amount)
        # print(response)
        # context = { 'response': response,}
        return render(request, 'refund.html')
    
    except TransbankError as e:
        print(e.message)
    return HttpResponseRedirect('') 
