#imports

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
import requests








# remember is code is for sandbox and after compeleting your test you have to add these changes:
# https://sandbox.shepa.com/api/v1/token ==> https://merchant.shepa.com/api/v1/token
# https://sandbox.shepa.com/api/v1/verify ==>  https://merchant.shepa.com/api/v1/verify

# and also you have to change api='sandbox' to your real api key which is something like : API Key = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
# this api ket must be provided by shepa supprt

# good luck


@login_required
def send_payment(request):
    if request.method == 'GET':
        try:
            
            name = ""
            nationality = ""
            plan = ""
            #price = request.GET.get('price')
            price = 1000
            email = ""
            #api = settings.SHEPA_API_KEY
            api = 'sandbox'
            url = f'https://sandbox.shepa.com/api/v1/token'
            
            print(f'Plan: {plan}\nPrice: {price}')

            # Example order object; replace with actual data as needed
            order = {
                "total": price,
                "billing": {
                    "first_name": name,
                    "last_name": name ,
                    "address_1": "123 Main St",
                    "city": "Tehran",
                    "state": "Tehran",
                    "postcode": "12345",
                    "country": nationality,
                    "email": email,
                    "phone": "9123333333"
                },
                "shipping": {
                    "first_name": name,
                    "last_name": name,
                    "address_1": "123 Main St",
                    "city": "Tehran",
                    "state": "Tehran",
                    "postcode": "12345",
                    "country": nationality,
                    "email": email,
                    "phone": "9123333333"
                },
                "products": [
                    {
                        "id": plan,
                        "name": plan,
                        "slug": plan,
                        "price": price,
                        "qty": 1,
                        "image": "http://example.com/product-1.jpg"
                    }
                    
                ]
            }

            data = {
                'api': api,
                'amount': price,
                'callback': f'http://{request.get_host()}/verify?plan={plan}&price={price}',
                'mobile': '9123333333',
                'email': email,
                'description': 'WritingChecker premium subscription' ,
                'order': order,
                'plan': plan
            }
            
            # Send the request with JSON payload
            response = requests.post(url, json=data)
            response_data = response.json()

            if response_data['success']:
                return redirect(response_data['result']['url'])
            else:
                return HttpResponse(f"<head><meta charset='utf-8'></head>{response_data['error']}")
        except Exception as e:
            return HttpResponse(f"<head><meta charset='utf-8'></head>{e}")
    else:
        return redirect('')




def verify_payment(request):
    if request.method == 'GET':
        token = request.GET.get('token')
        status = request.GET.get('status')

        user = ""
        plan = request.GET.get('plan')
        price = request.GET.get('price') 
      


        if status == "success":
            try:
                response = requests.post(
                    'https://sandbox.shepa.com/api/v1/verify',
                    json={
                        'token': token,
                        'amount': price,
                        'api': 'sandbox'
                    }
                )
                response_data = response.json()

                if response_data['success']:
                        # this means that payment is done and successful
                        # in this section you should add needed changes to user's database
                        # e.g. change payment status or update premium status
                        #
                        #
                        #
                        #


                    return HttpResponseRedirect('/payment-success/')
                


                else:
                    return HttpResponse(f"<head><meta charset='utf-8'></head>{response_data['errors']}")
            except Exception as e:
                return HttpResponse(f"<head><meta charset='utf-8'></head>{e}")
        else:
            HttpResponseRedirect('/payment-failed/')

    return HttpResponseRedirect('/payment-failed/')
            







def payment_success(request):
    return render(request, 'payment/payment_success.html')

def payment_failed(request):
    return render(request, 'payment/payment_failed.html')
