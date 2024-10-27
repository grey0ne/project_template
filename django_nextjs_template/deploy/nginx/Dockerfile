FROM nginx:1.26-alpine-slim

COPY ./deploy/nginx/conf/nginx_prod.conf /etc/nginx/nginx.conf
COPY ./backend/static /usr/share/nginx/static
