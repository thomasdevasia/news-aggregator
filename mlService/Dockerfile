FROM python:3.12.9-alpine

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt && \
  python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. ./aiChat.proto

CMD ["python", "./grpcServer.py"]
