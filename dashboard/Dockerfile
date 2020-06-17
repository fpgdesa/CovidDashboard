# Pull base image
FROM python:3.6
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set work directory
WORKDIR /code
# Install dependencies
COPY Pipfile Pipfile.lock /code/
RUN  pip install pipenv && \
     pipenv install --system && \
     pipenv install plotly==4.8.1 && \
     pipenv install pandas && \
     pipenv install cufflinks

 
# Copy project
COPY . /code/
