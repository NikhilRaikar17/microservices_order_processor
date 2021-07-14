import requests


class OrderInfoClient:
    @staticmethod
    def get_info(id):
        response = requests.request(method="GET", url=f'http://docker.for.mac.localhost:5000/order_info/{id}')
        if response.status_code == 401:
            return False
        order_info = response.json()
        return order_info
    
class ExecutionPriceClient:
    @staticmethod
    def calculate(order_id):
        response = requests.request(method="GET", url=f'http://docker.for.mac.localhost:5001/cal_execution_price/{order_id}')
        if response.status_code == 401:
            return False
