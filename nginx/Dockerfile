FROM nginx:latest

# Copy configuration files
COPY conf.d/ /etc/nginx/templates/
COPY entrypoint.sh /entrypoint.sh

# Make the script executable
RUN chmod +x /entrypoint.sh

# Check if file is executable
RUN if [ ! -x /entrypoint.sh ]; then echo "entrypoint.sh is not executable"; exit 1; fi

# Override the default command
CMD ["/entrypoint.sh"]
