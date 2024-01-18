FROM python:3.10

WORKDIR /app

COPY ./ /app

RUN pip3 install -r requirements.txt

EXPOSE 5000
#CMD [ "python3", "-m" , "flask", "run", "-h", "0.0.0.0"]
CMD ["python3", "app.py"]