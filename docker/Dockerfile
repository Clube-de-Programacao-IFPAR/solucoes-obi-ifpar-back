FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    python3 \
    gcc \
    g++ \
    default-jdk \
    nodejs \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m sandbox

WORKDIR /workspace

COPY docker/runner.py /runner.py
COPY docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

USER sandbox

ENTRYPOINT ["/entrypoint.sh"]