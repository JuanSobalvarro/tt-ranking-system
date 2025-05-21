FROM nginx:latest

# Copy configuration files
COPY conf.d/ /etc/nginx/templates/
COPY entrypoint.sh /entrypoint.sh

# Make the script executable
RUN chmod +x /entrypoint.sh

# Override the default command
CMD ["/entrypoint.sh"]
