FROM python:3.8
WORKDIR image-directory
RUN pip install flask
RUN pip install flask-pymongo
RUN pip install python-dotenv
RUN pip install -U flask-cors==3.0.10
COPY ./image-directory .
# RUN flask init-db
# EXPOSE 5000
CMD flask run --host=0.0.0.0