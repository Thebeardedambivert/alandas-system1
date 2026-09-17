FROM caddy:2.8.4-alpine

# Copy the fixed gateway policy into the image. Coolify's Compose runtime can
# otherwise create a directory for a missing bind-mount source and fail before
# Caddy has a chance to start.
COPY Caddyfile /etc/caddy/Caddyfile
