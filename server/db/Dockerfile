FROM postgres:15.7

ENV POSTGRES_DB=reminder_db
ENV POSTGRES_USER=reminder_user
ENV POSTGRES_PASSWORD=reminder

COPY ./init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
