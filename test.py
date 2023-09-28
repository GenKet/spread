import requests
from requests.auth import HTTPBasicAuth
import json

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-API-Version": "2",
}

basic = HTTPBasicAuth('25332', '79588228d9f50034fc476444807a8cb9d58b34f02504467aa18d5e001e4e9db4')

r = requests.get('https://api.bepaid.by/products/prd_2c7478647cf6bd3d',auth=basic )
r = r.json()
name = r["name"]
description = r["description"]
amount = r["amount"]
amount1 = float(amount/100)
currency = r["currency"]
# infinite = r["infinite"]
pay_url = r["pay_url"]
payment_url = r["payment_url"]
confirm_url = r["confirm_url"]
print(r)





data = {
    "checkout": {
        "transaction_type": "payment",
        "attempts": 3,
        "settings": {

            "return_url": "http://127.0.0.1:4567/return",
            "success_url": "http://127.0.0.1:4567/success",
            "decline_url": "http://127.0.0.1:4567/decline",
            "fail_url": "http://127.0.0.1:4567/fail",
            "cancel_url": "http://127.0.0.1:4567/cancel",
            "notification_url": "http://your_shop.com/notification",
            "button_text": f"Оплатить {amount1} {currency}",
            "button_next_text": "Вернуться в магазин",
            "language": "ru",
            "customer_fields": {
                "visible": ["first_name", "last_name","country","phone","birth_date","email"],
            },
        },
        "payment_method": {
            "types": ["credit_card"]
        },
        "order": {
            "currency": currency,
            "amount": amount,
            "description": description
        },
        "customer": {
    }
    }
}

r = requests.post('https://checkout.bepaid.by/ctp/api/checkouts', json=data, auth=basic, headers=headers)
print(r.text)
r = r.json()
token = r["checkout"]["token"]
url = r["checkout"]["redirect_url"]


r = requests.get(f"https://checkout.bepaid.by/ctp/api/checkouts/{token}", auth=basic)
print(url)
r = r.json()

status = r["checkout"]["status"]

print(status)

