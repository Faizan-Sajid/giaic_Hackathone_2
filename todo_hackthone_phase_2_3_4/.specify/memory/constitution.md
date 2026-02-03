<!-- Sync Impact Report -->
<!-- Version change: N/A → 1.0.0 -->
<!-- Modified principles: N/A (initial creation) -->
<!-- Added sections: All sections created from scratch -->
<!-- Removed sections: N/A -->
<!-- Templates requiring updates: ✅ plan-template.md (Constitution Check section compatible), ✅ spec-template.md (compatible), ✅ tasks-template.md (compatible) -->
<!-- Follow-up TODOs: None -->

# TaskFlow AI Constitution

## Core Principles

### I. Spec-First Development
All functionality MUST be defined in specifications before implementation. Code MUST be generated from specifications using Claude Code. Manual code changes are strictly prohibited unless explicitly permitted. If generated output is incorrect, revise the specification — NOT the code. Every code file MUST contain comments linking to Task IDs and Spec sections.

**Rationale:** Ensures reproducibility, version control of requirements, and AI agent alignment.

### II. AI as Controlled Executor
AI agents are implementation executors, NOT autonomous decision-makers. AI behavior MUST be constrained by specifications, MCP tools, and explicit contracts. AI agents MUST NOT directly access databases, infrastructure, or secrets. All AI actions must be auditable and traceable to specifications.

**Rationale:** Maintains human control over architecture and prevents "AI drift."

### III. Determinism and Reproducibility
System behavior must be predictable, testable, and reproducible. No implicit state, hidden logic, or undefined behavior allowed. All side effects (database writes, events, API calls) must be explicit. External dependencies must be version-pinned.

**Rationale:** Enables debugging, testing, and production reliability.

### IV. Production-Grade Standards
Architectural decisions must reflect real-world production systems. No demo shortcuts, mock-only logic, or non-scalable patterns. Follow 12-Factor App methodology where applicable. Security-first design in all phases.

**Rationale:** Prepares developers for real-world cloud-native development.

### V. Stateless Architecture Priority
Services MUST be stateless where possible. All session state MUST be externalized (database, cache). Enables horizontal scaling and container orchestration. Exception: In-memory state allowed ONLY in Phase I.

**Rationale:** Cloud-native systems require stateless services for scaling and resilience.

## Global Quality Standards

### Specification Standards
All Specifications MUST:
- Explicitly reference this Constitution in the preamble
- Define clear inputs, outputs, constraints, and acceptance criteria
- Be testable with measurable success criteria
- Use precise, unambiguous language (avoid "should," "might," "good")
- Include error handling specifications
- Define data validation rules explicitly

### Implementation Standards
All implementations MUST:
- Match the approved specification exactly — no creative deviations
- Use only Constitution-approved technology versions
- Implement fail-fast validation on all inputs
- Emit structured, JSON-serializable logs
- Surface errors clearly without exposing secrets or stack traces
- Include inline comments referencing Task IDs and Spec sections

### Security Standards
- All API endpoints MUST enforce authentication (except health checks)
- JWT tokens MUST be used for stateless authentication
- Token expiration MUST be enforced (max 7 days)
- User data isolation MUST be enforced at database query level
- NO hardcoded secrets, API keys, or credentials in code
- All secrets MUST be injected via environment variables
- Passwords MUST be hashed (bcrypt, minimum 12 rounds)
- Input validation MUST prevent SQL injection, XSS, and command injection

### Technology Baseline
Mandatory minimum versions:
- Python 3.13+ (backend)
- FastAPI 0.115.0+
- SQLModel 0.0.22+
- PostgreSQL 16+
- Node.js 22 LTS
- Next.js 15+
- TypeScript 5.7+
- Better Auth 1.0+
- Docker 27+
- Kubernetes 1.31+
- Helm 3.16+

### Code Quality Standards
- Python: Follow PEP 8, type hints on all functions, max 50 lines per function, 80% test coverage
- TypeScript: Strict mode, no `any` types, functional components, max 200 lines per component
- All public APIs MUST have OpenAPI/Swagger documentation

### Observability Standards
- Use structured logging (JSON format)
- Include correlation IDs for request tracing
- All services MUST expose `/health` endpoint
- Health checks MUST verify database connectivity, external services, and resource availability

## Phase-Specific Constraints

### Phase I — In-Memory Python Console Todo Application
- Technology: Python 3.13+, UV for package management
- Architecture: Single module or package with separated concerns (data layer, business logic, UI)
- Data: In-memory structures only (no file I/O)
- Prohibited: External databases, services, manual code writing, unvalidated inputs

### Phase II — Full-Stack Web Application with Authentication
- Technology: Next.js 15+ (frontend), FastAPI 0.115+ (backend), Neon PostgreSQL 16+, Better Auth 1.0+
- Architecture: Monorepo structure with `/frontend` and `/backend`
- API: RESTful endpoints under `/api/{user_id}/tasks`, JWT authentication on all endpoints
- Security: JWT secret environment-based, 7-day expiration max, user_id matching enforced
- Prohibited: JWT in localStorage, hardcoded secrets, missing user_id validation, manual SQL queries

### Phase III — AI-Powered Chatbot with MCP Architecture
- Technology: OpenAI ChatKit (frontend), FastAPI + OpenAI Agents SDK + MCP SDK (backend)
- Architecture: Stateless conversation flow with database-backed history
- MCP Tools: Must be stateless, accept user_id as first parameter, return structured JSON
- Prohibited: AI with direct database access, stateful agent memory, missing user_id validation in tools

### Phase IV — Local Kubernetes Deployment with Helm
- Technology: Docker 27+, Minikube 1.31+, Helm 3.16+, kubectl-ai, Kagent
- Architecture: Multi-pod deployment with Ingress, external Neon database
- Containerization: Multi-stage builds, non-root user, health checks, layer caching
- Prohibited: Hardcoded IPs/hostnames, missing health checks, unlimited resource requests

### Phase V — Advanced Cloud Deployment with Event-Driven Architecture
- Technology: Cloud Kubernetes (AKS/GKE/OKE), Kafka 3.9+, Dapr 1.14+, GitHub Actions
- Architecture: Event-driven microservices with Dapr building blocks (Pub/Sub, State Management, Service Invocation, Jobs API)
- Features: Priorities, Tags/Categories, Search & Filter, Recurring Tasks, Due Dates & Reminders
- Prohibited: Missing user_id validation, secrets in ConfigMaps, manual kubectl without specs

## Development Workflow

### Code Review Requirements
- All PRs must verify constitutional compliance
- Complexity must be justified
- Use .specify/ templates for spec-driven development

### Testing Gates
- Phase I: Code passes type checking (mypy)
- Phase II: Integration tests for authentication flow, E2E test for critical user journey
- Phase III: MCP tools work correctly and securely, AI cannot access other users' data
- Phase IV: Application survives pod restarts, all pods healthy
- Phase V: Event-driven architecture validated, Dapr integration tested

### Deployment Approval Process
- Code must be generated from specifications using Claude Code
- All constitutional requirements must be verified
- Deployment requires updated specs, tests, and documentation

## Governance

### Amendment Process
- This Constitution defines immutable, project-wide quality standards
- Hierarchy of Authority: Constitution > Phase-specific specifications > Feature specifications > Implementation tasks
- Amendments require documentation, approval, and migration plan
- Every Specification, Plan, Task, and Implementation MUST comply with this Constitution

### Versioning Policy
- MAJOR: Backward incompatible governance/principle removals or redefinitions
- MINOR: New principle/section added or materially expanded guidance
- PATCH: Clarifications, wording, typo fixes, non-semantic refinements

### Compliance Review
- All PRs/reviews must verify compliance with this Constitution
- Complexity must be justified with architectural reasoning
- Use CLAUDE.md and AGENTS.md for runtime development guidance

**Version**: 1.0.0 | **Ratified**: 2026-01-05 | **Last Amended**: 2026-01-05
