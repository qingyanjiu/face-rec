FROM qingyanjiu/face-rec:latest
RUN python package.py
ADD dist/* /app/
WORKDIR /app
CMD gunicorn -b :5000 api:app