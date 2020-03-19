FROM nginx:alpine
COPY ./build /usr/share/nginx/html
COPY ./vhosts.conf /etc/nginx/conf.d/vhosts.conf
RUN chmod -R 777 /usr/share/nginx/