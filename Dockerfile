FROM --platform=linux/amd64 python:3.7-slim as base

WORKDIR /app

# Install system dependencies required for forexconnect
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy local dependencies
COPY libs/forexconnect-1.6.43-cp37-cp37m-manylinux1_x86_64.whl /tmp/

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir /tmp/forexconnect-1.6.43-cp37-cp37m-manylinux1_x86_64.whl && \
    pip install --no-cache-dir -r requirements.txt

FROM base as production

# Create prod user
RUN groupadd --gid 1000 prod-user \
    && useradd --uid 1000 --gid prod-user --shell /bin/bash --create-home prod-user

# Copy application code
COPY --chown=prod-user:prod-user app /app/app

# Switch to user
USER prod-user

# Set python path
ENV PYTHONPATH=/app

CMD ["uvicorn", "app.entrypoints.fastapi.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM base as development

# devcontainer dependencies and utils
RUN apt-get update && apt-get install --no-install-recommends -y \
    sudo git bash-completion vim ssh wget which \
    procps libatomic1 \
    && rm -rf /var/lib/apt/lists/*

# Create devcontainer user and add it to sudoers
RUN groupadd --gid 1000 dev-user \
    && useradd --uid 1000 --gid dev-user --shell /bin/bash --create-home dev-user \
    && echo dev-user ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/dev-user \
    && chmod 0440 /etc/sudoers.d/dev-user

# Copy application code
COPY app /app/app

# Set python path
ENV PYTHONPATH=/app
