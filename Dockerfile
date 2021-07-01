FROM python:3.6.5

RUN pip install Jinja2==2.10 MarkupSafe==1.0 honcho==1.0.1

ENTRYPOINT [ "honcho" ]
