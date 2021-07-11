FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /calculate_order
COPY requirements.txt /calculate_order/requirements.txt
RUN pip install -r requirements.txt
COPY . /calculate_order