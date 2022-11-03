# Use nginx image and set nginx configuration file
FROM nginx:stable-alpine
COPY nginx.default.conf /etc/nginx/conf.d/default.conf

# Build step #2: build the API with the client as static files
FROM python:3.9
RUN mkdir ./api
COPY . ./api/

RUN pip install -r ./api/requirements.txt
ENV FLASK_DEBUG False

EXPOSE  5000
WORKDIR /api
CMD ["gunicorn", "-b", ":5000", "app:app"]
