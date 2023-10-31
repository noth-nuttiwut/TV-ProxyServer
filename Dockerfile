FROM python:3.10.12-slim


WORKDIR /ProxyServer


COPY ./requirements.txt /ProxyServer/requirements.txt


RUN pip install --upgrade pip


RUN pip install --no-cache-dir --upgrade -r /ProxyServer/requirements.txt


COPY ./app /ProxyServer/app


CMD uvicorn app.main:app --host=0.0.0.0 --port=$PORT
