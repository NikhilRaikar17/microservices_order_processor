import requests

class OrderInfoClient:
    @staticmethod
    def get_info(id):
        try:
            if not type(id) is int:
                raise Exception('Invalid order_id passed')

            response = requests.request(method="GET", url=f'http://docker.for.mac.localhost:5000/order_info/{id}')
            if response.status_code!= 200:
                raise Exception('Invalid order_id passed or resource cannot be found')
            
            order_info = response.json()
            return order_info
        except Exception as e:
            message = e.args[0]
            print(message)
            return {'quantity': None}
    
class ExecutionPriceClient:
    @staticmethod
    def calculate(order_id):
        try:
            if not type(order_id) is int:
                raise Exception('Invalid order_id passed')

            response = requests.request(method="GET", url=f'http://docker.for.mac.localhost:5001/cal_execution_price/{order_id}')
            if response.status_code != 200:
                raise Exception('Response from request is broken')
        except Exception as e:
            message = e.args[0]
            print(message)
            return {'ERROR': message}
