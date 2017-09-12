FROM python:3.6

# cache the freaking requirements.txt
RUN mkdir /code
COPY requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt
RUN rm /code/requirements.txt

COPY . /code

VOLUME /code

ENTRYPOINT ["python"]
CMD ["-u", "/code/twitter.py"]
