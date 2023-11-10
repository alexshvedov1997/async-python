FROM nginx


RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/
COPY ./configs/site.conf /etc/nginx/conf.d/
RUN  mkdir -p /var/www


RUN chown www-data:www-data /var/www 
RUN chmod -R 777 /var/www