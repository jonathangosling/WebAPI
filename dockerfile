FROM public.ecr.aws/lambda/python:3.8
COPY ./requirements.txt    /requirements.txt
COPY ./main.py     /main.py
COPY ./html_files /html_files
RUN pip install -r /requirements.txt
CMD ["/main.handler"]
