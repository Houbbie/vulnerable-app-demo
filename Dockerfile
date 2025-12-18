FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl git && apt-get clean
RUN curl -sSfL https://raw.githubusercontent.com/trufflehog-group/trufflehog/main/scripts/install.sh | sh -s -- -b /usr/local/bin

# CRUCIALE FIX: Vertel Git dat de /app map veilig is om te scannen
RUN git config --global --add safe.directory /app

WORKDIR /app
COPY hunter.py .
CMD ["python", "hunter.py"]