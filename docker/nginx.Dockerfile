FROM nginx:latest

ENV NGINX_ENVSUBST_OUTPUT_DIR=/etc/nginx/

COPY nginx.conf.template /etc/nginx/templates/nginx.conf.template