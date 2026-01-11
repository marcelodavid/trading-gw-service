# 001. FXCM Service Segregation

Date: 2025-12-26

## Status

Accepted

## Context

The trading system needs to integrate with FXCM through their `forexconnect` Python SDK. However, this SDK has strict constraints:
- It only supports Python 3.7.
- The available wheel is built for `linux/amd64`.
- The main trading system or other microservices might want to use newer Python versions or run natively on ARM64 architectures (e.g., Apple Silicon for development).

Including `forexconnect` directly in the core services forces the entire codebase to adhere to these outdated constraints.

## Decision

We will decouple the FXCM integration into a dedicated microservice named `trading-gateway` (initially scoped for FXCM but designed to be a generic gateway).

- **Architecture**: The service will be containerized using Docker, explicitly targeting `platform: linux/amd64`.
- **Communication**: It will expose a REST API (FastAPI) for other services to consume.
- **Dependency Management**: The `forexconnect` wheel will be installed directly within this service's environment.

## Consequences

### Positive
- The main system can use modern Python versions and run on any architecture.
- FXCM dependencies are isolated.
- The gateway can be extended for other legacy/specific broker SDKs.

### Negative
- Increased operational complexity (one more service to manage).
- Potential performance overhead due to network calls (though running on localhost or same network minimizes this).
- Cross-platform build/emulation overhead when developing on ARM machines.
