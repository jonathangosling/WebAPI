FROM public.ecr.aws/lambda/python:3.8
COPY ./requirements.txt    /requirements.txt
COPY ./main.py     /main.py
COPY ./Front_Page.txt /Front_Page.txt
RUN pip install -r /requirements.txt
CMD ["/main.handler"]
