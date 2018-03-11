FROM python:3.6

RUN apt-get update && apt-get install postgresql-client-9.4 -y

COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
ENV PYTHONPATH=/opt/webapp

# add app code
ADD . /opt/webapp/
WORKDIR /opt/webapp

# Run the image as a non-root user
RUN useradd -m flat-box
USER flat-box

CMD gunicorn --bind 0.0.0.0:$PORT server
