# import razorpay
# from django.conf import settings

# def process_payment(amount):
#     print('*****************************')
#     client = razorpay.Client(auth=('rzp_test_0wKkzO70vA65D5', 'FLpfPU5ERtHc4zxTY6LvDRJJ'))
#     print('*****************************')
#     print(client)
#     order_amount = amount * 100  # Convert amount to paise
#     order_currency = 'INR'  # Change according to your currency
#     order_receipt = 'order_receipt'  # Change to a unique order ID or receipt number

#     # Create a Razorpay order
#     data = {
#         'amount': order_amount,
#         'currency': order_currency,
#         'receipt': order_receipt,
#         # Add more options if required
#     }
#     order = client.order.create(data=data)

#     return order
