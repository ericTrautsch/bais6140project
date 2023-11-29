# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app
ENV PORT=8050
# Install Poetry
RUN pip install poetry

# Copy poetry dependent files
COPY pyproject.toml /usr/src/app
COPY poetry.lock /usr/src/app

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Make port 8050 available to the world outside this container
EXPOSE ${PORT}

# Copy the current directory contents into the container at /usr/src/app
COPY ./src /usr/src/app/src
COPY app.py /usr/src/app
COPY ./assets /usr/src/app/assets
COPY ./data /usr/src/app/data

# Run app.py when the container launches
CMD ["python", "./app.py"]
