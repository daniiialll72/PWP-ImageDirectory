FROM python:3.8
COPY . /app/
WORKDIR /app
RUN ls
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 5001
CMD gunicorn --worker-class gevent --workers 8 --bind 0.0.0.0:5001 wsgi:app --max-requests 10000 --timeout 5 --keep-alive 5 --log-level info