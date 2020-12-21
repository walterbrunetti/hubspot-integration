FROM python:3.8.0-alpine AS build

ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.8.0-alpine
COPY --from=build /usr /usr

WORKDIR /app

COPY . ./

EXPOSE 8000

CMD ["python", "hubspot_integration_app/manage.py", "runserver", "0.0.0.0:8000"]
