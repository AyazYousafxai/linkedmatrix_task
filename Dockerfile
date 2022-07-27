FROM python:3.6
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /matrix
COPY requirements.txt /matrix/
RUN pip install -r requirements.txt
COPY . /matrix/