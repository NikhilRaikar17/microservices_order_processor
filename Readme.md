# UltraTendency Microservices Task

This is a order processing task. There are two micro services, one to push the orders into the database and the other is responsible to collect that order and process and perform calculations on them. These microservice internally communicate through RabbitMQ.

## Project Structure
The Python Flask based microservices project is composed of the following: 
* [Database]()
* [Order-generator-service]()
* [Order-processor-service]()

## Microservices Setup and Configuration
To launch the end-to-end microservices application perform the following:

### Step 1.
Create a new Docker network and name it ```micro_network```:
```
docker network create micro_network
```
### Step 2.
Set up network
```
docker network create micro_network
```
#### order_generator_service
```
cd order_generator_service
docker-compose up --build
```

#### order_processor_service
```
cd order_processor_service
docker-compose up --build
```

#### database
```
cd database
docker-compose up --build
```
### Step 3.
Create database tables for order_generator_service
```
docker-compose exec order_generator_service sh
```

Open python shell by typing "python" in the cmd line
```
python
from order_generator_service import db
db.create_all()
exit()
```


Create database tables for order_processor_service
```
docker-compose exec order_processor_service sh
```
Open python shell by typing "python" in the cmd line
```
python
from order_processor_service import db
db.create_all()
exit()
```
### Step 4.
Using browser you can now start the process by accessing the links
```
http://localhost:5000/
```
You can see in the standard out of the order_processor_service container the "OrderExecutionPrice" is getting printed
and also in the "order_generator_service" container the order_id getting printed.

You can access the average execution price and total orders processed information using the below link
```
localhost:5001/metrics
```
You can also stop processing all of the orders by accessing the below link
```
http://localhost:5000/stop_order
```
Please note, once the above link is executed the scheduler is killed. In order to restart the scheduler, you need to restart your containers from the beginning and start the whole process all over again. 

There is no restart functionality which has been added.

You can also choose to truncate the created database tables using the below link

```
http://localhost:5000/truncate_table

http://localhost:5001/truncate_table
```
Truncate will delete all of the present data already present in the database tables and will not delete the table.