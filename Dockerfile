FROM python:3.11-bookworm

WORKDIR /app
# In Azure, Azure app service with python is Linux host and libmagic-dev
# is required on the linux host vm for permhash to work
RUN apt update && apt install libmagic-dev

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 13337

CMD ["python", "app.py"]