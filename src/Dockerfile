FROM python:3.8
WORKDIR image-directory
RUN pip install flask
pip install mongoengine
RUN pip install python-dotenv
pip3 install minio
RUN pip install -U flask-cors==3.0.10
COPY ./image-directory .
# RUN flask init-db
# EXPOSE 5000
CMD flask run --host=0.0.0.0