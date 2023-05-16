FROM qingyanjiu/face-rec:latest AS build
ADD . /app/
WORKDIR /app
RUN python package.py

FROM qingyanjiu/face-rec:latest
COPY --from=build /app/dist/* /app/
WORKDIR /app
EXPOSE 5000
CMD gunicorn -b :5000 api:app