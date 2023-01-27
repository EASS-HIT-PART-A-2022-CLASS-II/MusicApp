FROM python:3.9-slim

# Install SQLite
RUN apt-get update \
    && apt-get install -y sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy the musicapp.db file to the container
COPY musicapp.db /data/

# Expose the SQLite server port
EXPOSE 8888

# Run the SQLite server
# CMD ["sqlite3", "/data/musicapp.db", ".timeout", "10000", ".mode", "column", ".headers", "on", ".server", "localhost"]
ENTRYPOINT ["./entrypoint.sh"]