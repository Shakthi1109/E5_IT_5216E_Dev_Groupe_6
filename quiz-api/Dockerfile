FROM python:3.10

WORKDIR /app

COPY ./ /app

RUN pip3 install -r requirements.txt

EXPOSE 5000
#CMD [ "python3", "-m" , "flask", "run", "-h", "0.0.0.0"]
CMD ["python3", "app.py"]

# docker build -t quiz-api .
# docker run -d -p 5000:5000 [ID_Image]
# docker logs -f [ID_Container]
