import unittest
import requests
import sys
import time
import random
import docker
import pymysql

class OrderGenerateAndProccess(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            list_running_containers = ['order_processor','order_processor_queue','order_generator','database']
            client = docker.from_env()
            containers = client.containers.list()

            if len(containers)<1:
                raise Exception("""No docker containers running, please start the containersand run the tests again\n
                to start the containers, please have a look into the ReadMe.md""")

            for container in containers:
                container_name = container.name
                if container_name in list_running_containers:
                    index = list_running_containers.index(container_name)
                    list_running_containers.pop(index)

            if len(list_running_containers) > 0:
                for name in list_running_containers:
                    raise Exception(f"{name} is not running, please start this container to proceed further in running test cases""")
            
            connection = pymysql.connect(host='localhost',
                                        user='root',
                                        password='root',
                                        database='main',
                                        port=33067
                                        )
            cur = connection.cursor()
            cur.execute("TRUNCATE TABLE Orders")
            cur.execute("TRUNCATE TABLE order_process")

        except Exception as e:
            message = e.args[0]
            print(e)
            sys.exit(message)

    def test_01_orders(self):
        response = requests.request(method="GET", url='http://localhost:5000/')
        time.sleep(20)
        self.assertEqual(response.status_code, 200)

    def test_02_response_200_order_info(self):
        example_order_id = random.randint(1,4)
        response=requests.request(method="GET", url=f'http://localhost:5000/order_info/{example_order_id}')
        self.assertEqual(response.status_code, 200)
    
    def test_03_response_404_order_info(self):
        example_string = 'hajsd' 
        response=requests.request(method="GET", url=f'http://localhost:5000/order_info/{example_string}')
        self.assertEqual(response.status_code,404)
    
    def test_04_response_404_execution_price(self):
        example_string = 'hajsd' 
        response=requests.request(method="GET", url=f'http://localhost:5001/cal_execution_price/{example_string}')
        self.assertEqual(response.status_code,404)
    
    def test_05_execution_price(self):
        example_order_id = random.randint(1,4)
        response = requests.request(method="POST", url=f'http://localhost:5001/cal_execution_price/{example_order_id}')
        self.assertEqual(response.status_code,200)
    
    def test_06_metrics(self):
        response=requests.request(method="GET", url='http://localhost:5001/metrics')
        self.assertEqual(response.status_code,200)
    
    @classmethod
    def tearDownClass(cls):
        list_running_containers = ['order_processor','order_processor_queue','order_generator','database']
        client = docker.from_env()
        containers = client.containers.list()
        for container in containers:
            container_name = container.name
            if container_name in list_running_containers:
                index = list_running_containers.index(container_name)
                list_running_containers.pop(index)
                container.restart()


if __name__ == '__main__':
    unittest.main(failfast = True)