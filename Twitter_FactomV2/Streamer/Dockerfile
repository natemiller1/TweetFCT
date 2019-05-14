FROM python:3
RUN mkdir /code
WORKDIR /code
ADD Tweet_WriterV1.py /code/
COPY requirements.txt /code/
RUN pip install -r requirements.txt
CMD [ "python", "Tweet_WriterV1.py", "1088451823642595328" ]
Copy . /code/