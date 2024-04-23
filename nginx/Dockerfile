FROM nginx:1.21.5-alpine

RUN apk update && \
    apk add --no-cache certbot certbot-nginx

COPY ./default.conf /etc/nginx/conf.d/default.conf

# Expose ports
EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]
