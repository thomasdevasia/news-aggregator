FROM python:3.10-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY . /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt && \
  python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. ./aiChat.proto

CMD fastapi dev server.py --port 8002 --host 0.0.0.0
