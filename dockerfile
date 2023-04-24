#FROM public.ecr.aws/lambda/python:3.8
FROM python:3.10
COPY ./requirements.txt    /requirements.txt
COPY ./main.py     /main.py
ADD ./imgs/ /imgs/
RUN pip install -r /requirements.txt
#CMD ["/main.handler"]
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","80"]
