FROM php:7-fpm

RUN apt-get update \
    && docker-php-ext-install pdo_mysql

RUN apt-get install -y --no-install-recommends \
    libsqlite3-dev \
    ruby-dev

RUN gem install mailcatcher
