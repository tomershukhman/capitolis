#
FROM tomershukhman/weatherapp-base:latest

#
WORKDIR /code

# Set build argument
ARG BUILD_NUMBER

# Set environment variable
ENV BUILD_NUMBER=${BUILD_NUMBER}

#
COPY ./app /code/app

#
CMD ["fastapi", "run", "app/main.py", "--port", "80"]