#
FROM python:3.9

#
WORKDIR /code

# Set build argument
ARG BUILD_NUMBER

# Set environment variable
ENV BUILD_NUMBER=${BUILD_NUMBER}

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./app /code/app

#
CMD ["fastapi", "run", "app/main.py", "--port", "80"]