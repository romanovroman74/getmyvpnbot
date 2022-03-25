import config
from yoomoney import Client
from yoomoney import Quickpay

client = Client(config.yoomoney_token)
user = client.account_info()

def gen_invoice_url(sum, target, order_id):
    quickpay = Quickpay(
                receiver=config.receiver,
                quickpay_form="shop",
                targets=f"{target}",
                paymentType="SB",
                sum=f"{sum}",
                label=f"{order_id}"
                )
    data = quickpay.redirected_url
    return data

#Проверка оплаты
def check_payment(order_id):
    history = client.operation_history(label=f"{order_id}")
    for operation in history.operations:
        result = operation.status
        if result == 'success':
            data = 'true'
            return data
        else:
             data = 'false'
             return data


def test():
    history = client.operation_history()
    for operation in history.operations:
        print()
        print("Operation:",operation.operation_id)
        print("\tStatus     -->", operation.status)
        print("\tDatetime   -->", operation.datetime)
        print("\tTitle      -->", operation.title)
        print("\tPattern id -->", operation.pattern_id)
        print("\tDirection  -->", operation.direction)
        print("\tAmount     -->", operation.amount)
        print("\tLabel      -->", operation.label)
        print("\tType       -->", operation.type)

