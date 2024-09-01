'''import requests
​
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer P4scCjwRomCsQl4PbeMNoVz7SJ7r'
}
​
payload = {
    "BusinessShortCode": 174379,
    "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjQwMzIyMjEzNDAy",
    "Timestamp": "20240322213402",
    "TransactionType": "CustomerPayBillOnline",
    "Amount": 1,
    "PartyA": 254742273610,
    "PartyB": 174379,
    "PhoneNumber": 254742273610,
    "CallBackURL": "https://api.darajambili.com/express-payment",
    "AccountReference": "CompanyXLTD",
    "TransactionDesc": "millan stragg" 
  }
​
response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, data = payload)
print(response.text.encode('utf8'))'''