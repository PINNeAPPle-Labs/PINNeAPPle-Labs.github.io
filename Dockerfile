# Static site, no build step. Multi-stage is unnecessary: nginx serves the tree.
FROM nginx:alpine
COPY . /usr/share/nginx/html
RUN rm -rf /usr/share/nginx/html/.git /usr/share/nginx/html/Dockerfile
EXPOSE 80
