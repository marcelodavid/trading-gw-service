# Trading Gateway Service

This service acts as a unified gateway for various trading brokers. Ideally, it provides a broker-agnostic API to clients.

## Architecture

This service is designed to run on `linux/amd64` architecture specifically because of the `forexconnect` (FXCM) dependency which only supports Python 3.7 on amd64 linux.

### Brokers

- **FXCM**: Implemented using `forexconnect` SDK.

## Setup

### Prerequisites

- Docker
- The `forexconnect` wheel file must be present in `libs/`.

### Docker Usage

The Dockerfile supports multi-stage builds (`development` and `production`).

#### Development

The `docker-compose.yml` is configured to target the `development` stage by default. This stage runs as `root` (for easy tool usage) and includes development utilities.

```bash
docker-compose up --build
```

#### Production

The `production` stage runs as a non-root user (`prod-user`) and contains only the necessary runtime dependencies.

**Build:**
```bash
docker build --target production --platform linux/amd64 -t trading-gateway:prod .
```

**Run:**
```bash
docker run --platform linux/amd64 -p 8000:8000 --env-file .env trading-gateway:prod
```

## API

The API is exposed at `http://localhost:8000`.
Docs available at `http://localhost:8000/docs`.

### Limitations

- **Python 3.7**: Required by FXCM SDK.
- **AMD64 Only**: Cannot run natively on ARM (Apple Silicon) without emulation.
