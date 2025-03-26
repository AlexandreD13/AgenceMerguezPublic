###########
# BUILDER #
###########

FROM python:3.11.4-slim-buster as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

# install python dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

FROM python:3.11.4-slim-buster

# Install nginx and supervisor
RUN apt -y update && apt install -y nginx supervisor

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

# copy entrypoint.sh
COPY deployment/entrypoint.sh $APP_HOME/entrypoint.sh
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

# Copy other configuration files for Nginx...
ARG SUPERVISOR_FILE=supervisor-website.conf
COPY deployment/$SUPERVISOR_FILE /etc/supervisor/conf.d/supervisor-app.conf
COPY deployment/nginx.conf /etc/nginx/nginx.conf
COPY deployment/nginx-app.conf /etc/nginx/sites-available/default

# Create folder for static files collected
RUN mkdir -p /home/app/web/static
#RUN rm /etc/nginx/conf.d/default.conf

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
#USER app
EXPOSE $PORT

ENTRYPOINT ["/home/app/web/entrypoint.sh"]

CMD ["supervisord", "-n", "-c", "/etc/supervisor/conf.d/supervisor-app.conf"]
