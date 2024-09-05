FROM nginx:1.26-alpine-slim

COPY ./nginx/conf/nginx.template /etc/nginx/nginx.template
COPY ./backend/static /usr/share/nginx/static

CMD /bin/sh -c "envsubst '\$DOMAIN' < /etc/nginx/nginx.template > /etc/nginx/nginx.conf && nginx -g 'daemon off;'"
