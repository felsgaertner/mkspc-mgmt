FROM python:3.8-alpine

RUN apk add --no-cache gcc libc-dev linux-headers

# install pypi packages
COPY . /django_project
RUN pip install --upgrade pip
RUN pip install ./django_project
RUN pip install uWSGI==2.0.21

COPY docker/app/uwsgi.ini /uwsgi.ini
COPY docker/app/scripts /scripts
RUN chmod -R +x /scripts
ENV PATH="/scripts:/py/bin:$PATH"

CMD ["run.sh"]
