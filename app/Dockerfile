FROM python:3.11-bookworm

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt


COPY __init__.py ./__init__.py
COPY main.py ./main.py
COPY app ./app

CMD ["fastapi", "run", "main.py", "--port", "80"]

