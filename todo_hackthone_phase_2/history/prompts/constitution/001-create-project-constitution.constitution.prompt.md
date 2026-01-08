---
id: 001
title: create project constitution
stage: constitution
date: 2026-01-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 1-jwt-todo-auth
user: user
command: /sp.constitution
labels: [constitution, setup]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:

## Prompt

# Constitution — Hackathon II: Spec-Driven AI-Native Todo System

## 1. Purpose & Product Vision

### 1.1 Product Definition
This project builds **"TaskFlow AI"** — an AI-native, cloud-native todo management system that evolves from a simple console application to a distributed, event-driven chatbot platform deployed on Kubernetes.

**Core Value Proposition:**
- Natural language task management through conversational AI
- Multi-user support with complete data isolation
- Event-driven architecture for scalability
- Cloud-native deployment patterns
- Production-grade security and observability

### 1.2 Constitutional Authority
This Constitution defines immutable, project-wide quality standards that apply to ALL work across ALL phases. It establishes non-negotiable rules governing:
- Specification quality and structure
- AI agent behavior and constraints
- Architecture discipline and patterns
- Security boundaries and authentication
- Technology versions and constraints
- Verification and acceptance standards

Every Specification, Plan, Task, and Implementation MUST comply with this Constitution.

**Hierarchy of Authority:**
1. Constitution (this document) — supreme authority
2. Phase-specific specifications
3. Feature specifications
4. Implementation tasks

---

## 2. Core Principles (Non-Negotiable)

### 2.1 Spec-First Development
- **All functionality MUST be defined in specifications before implementation**
- Code MUST be generated from specifications using Claude Code
- Manual code changes are **strictly prohibited** unless explicitly permitted
- If generated output is incorrect, revise the specification — NOT the code
- Every code file MUST contain comments linking to Task IDs and Spec sections

**Rationale:** Ensures reproducibility, version control of requirements, and AI agent alignment.

### 2.2 AI as Controlled Executor
- AI agents are implementation executors, NOT autonomous decision-makers
- AI behavior MUST be constrained by specifications, MCP tools, and explicit contracts
- AI agents MUST NOT directly access databases, infrastructure, or secrets
- All AI actions must be auditable and traceable to specifications

**Rationale:** Maintains human control over architecture and prevents "AI drift."

### 2.3 Determinism and Reproducibility
- System behavior must be predictable, testable, and reproducible
- No implicit state, hidden logic, or undefined behavior allowed
- All side effects (database writes, events, API calls) must be explicit
- External dependencies must be version-pinned

**Rationale:** Enables debugging, testing, and production reliability.

### 2.4 Production-Grade Standards
- Architectural decisions must reflect real-world production systems
- No demo shortcuts, mock-only logic, or non-scalable patterns
- Follow 12-Factor App methodology where applicable
- Security-first design in all phases

**Rationale:** Prepares developers for real-world cloud-native development.

### 2.5 Stateless Architecture Priority
- Services MUST be stateless where possible
- All session state MUST be externalized (database, cache)
- Enables horizontal scaling and container orchestration
- Exception: In-memory state allowed ONLY in Phase I

**Rationale:** Cloud-native systems require stateless services for scaling and resilience.

---

## 3. Global Quality Standards (Apply to ALL Phases)

### 3.1 Specification Standards

All Specifications MUST:
- **Explicitly reference this Constitution** in the preamble
- Define clear inputs, outputs, constraints, and acceptance criteria
- Be testable with measurable success criteria
- Use precise, unambiguous language (avoid "should," "might," "good")
- Include error handling specifications
- Define data validation rules explicitly

**Format Requirements:**
```markdown
# Feature: [Name]
## Constitutional Compliance
Inherits: Constitution v1.0
Applies to: Phase [X]

## User Stories
## Acceptance Criteria
## API Contracts (if applicable)
## Error Handling
## Security Considerations
```

❌ **Vague:** "System should be fast"
✅ **Testable:** "API P95 response time ≤ 300ms under 100 concurrent users"

---

### 3.2 Implementation Standards

All implementations MUST:
- **Match the approved specification exactly** — no creative deviations
- Use only Constitution-approved technology versions (see Section 3.4)
- Implement fail-fast validation on all inputs
- Emit structured, JSON-serializable logs (no plain text logs in production)
- Surface errors clearly without exposing secrets or stack traces to users
- Include inline comments referencing Task IDs and Spec sections

**Example:**
```python
# [Task: T-042] [Spec: task-crud.md §3.2]
# Implements task creation with user isolation
async def create_task(user_id: str, title: str):
    ...
```

**Prohibited Practices:**
- Manual patching of AI-generated code without spec updates
- Hardcoded configuration values
- Implicit error handling (silent failures)
- Non-deterministic behavior (random IDs without seeding, etc.)

---

### 3.3 Security Standards (Global)

#### 3.3.1 Authentication & Authorization
- **All API endpoints MUST enforce authentication** (except health checks)
- JWT tokens MUST be used for stateless authentication
- Token expiration MUST be enforced (max 7 days)
- User data isolation MUST be enforced at the database query level
- No user may access another user's data under any circumstance

#### 3.3.2 Secrets Management
- **NO hardcoded secrets, API keys, or credentials in code**
- All secrets MUST be injected via environment variables
- Environment variables MUST be documented in `.env.example`
- Kubernetes secrets MUST be used in Phases IV & V
- API keys MUST use prefix notation (e.g., `sk_prod_...`) for leak detection

#### 3.3.3 Data Protection
- Passwords MUST be hashed (bcrypt, minimum 12 rounds)
- Database connection strings MUST use TLS in production
- CORS policies MUST be explicitly defined (no `*` wildcard in production)
- Input validation MUST prevent SQL injection, XSS, and command injection

#### 3.3.4 Error Handling
- Error messages MUST NOT expose:
  - Stack traces
  - Database schema details
  - File paths
  - Internal service names
- Log sensitive errors server-side with correlation IDs
- Return generic errors to clients (e.g., "Operation failed. Ref: abc-123")

---

### 3.4 Technology Baseline (Mandatory Versions)

Unless explicitly overridden by a phase-specific specification, use:

| Technology | Minimum Version | Rationale |
|-----------|----------------|-----------|
| **Python** | 3.13+ | Latest stable with performance improvements |
| **UV** | Latest | Modern Python package manager |
| **FastAPI** | 0.115.0+ | Latest with OpenAPI 3.1 support |
| **SQLModel** | 0.0.22+ | Latest with improved async support |
| **PostgreSQL** | 16+ | Latest stable with performance improvements |
| **Node.js** | 22 LTS | Active LTS with latest features |
| **Next.js** | 15+ | Latest with improved App Router |
| **TypeScript** | 5.7+ | Latest stable |
| **Better Auth** | 1.0+ | Modern authentication library |
| **OpenAI Agents SDK** | Latest | Required for Phase III |
| **Official MCP SDK** | Latest | Required for Phase III |
| **Docker** | 27+ | Latest stable |
| **Kubernetes** | 1.31+ | Latest stable |
| **Helm** | 3.16+ | Latest stable |
| **Dapr** | 1.14+ | Latest stable |
| **Kafka** | 3.9+ (or Redpanda) | Latest stable |

**Prohibited Technologies:**
- Deprecated or EOL versions
- Experimental/alpha releases in production phases
- Technologies not listed without constitutional amendment

---

### 3.5 Code Quality Standards

#### 3.5.1 Python (Backend)
- Follow PEP 8 style guide
- Use type hints for all function signatures
- Maximum function length: 50 lines
- Maximum file length: 500 lines
- Use async/await for all I/O operations
- Minimum test coverage: 80%

#### 3.5.2 TypeScript (Frontend)
- Use strict mode (`"strict": true` in tsconfig.json)
- No `any` types without explicit justification
- Use functional components (React)
- Maximum component length: 200 lines
- Follow Airbnb style guide

#### 3.5.3 Documentation
- All public APIs MUST have OpenAPI/Swagger documentation
- README.md MUST include:
  - Setup instructions
  - Environment variables
  - Running instructions
  - Testing instructions
- CLAUDE.md MUST reference AGENTS.md

---

### 3.6 Observability Standards

#### 3.6.1 Logging
- Use structured logging (JSON format)
- Include correlation IDs for request tracing
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Never log sensitive data (passwords, tokens, PII)

#### 3.6.2 Health Checks
- All services MUST expose `/health` endpoint
- Health checks MUST verify:
  - Database connectivity
  - External service availability
  - Resource availability (memory, disk)

#### 3.6.3 Metrics (Phases IV & V)
- Expose Prometheus-compatible metrics
- Track: request rate, error rate, response time, resource usage

---

## 4. Phase-Specific Constitutional Constraints

---

## PHASE I — In-Memory Python Console Todo Application

### 4.1.1 Phase Objective
Build a command-line todo application demonstrating spec-driven development fundamentals and clean code principles.

### 4.1.2 Mandatory Requirements

**Technology Stack:**
- Python 3.13+
- UV for package management
- No external databases or services
- In-memory data structures only

**Functional Requirements:**
- Add task (title + description)
- List all tasks
- Update task (modify title/description)
- Delete task by ID
- Mark task as complete/incomplete

**Architectural Constraints:**
- Single Python module or clean package structure
- Separation of concerns (data layer, business logic, UI)
- Data persistence through in-memory lists/dictionaries
- No file I/O unless specified

**Quality Standards:**
- Type hints on all functions
- Docstrings for all public functions
- Input validation (non-empty titles, valid IDs)
- Clear error messages for invalid operations
- Deterministic task IDs (incremental integers)

**Deliverables:**
- Constitution file (this document)
- `/specs` folder with all specification files
- `/src` folder with Python source code
- `README.md` with setup instructions
- `CLAUDE.md` referencing AGENTS.md
- `AGENTS.md` with agent instructions

**Acceptance Criteria:**
- All basic features work as specified
- No runtime errors for valid inputs
- Clear error messages for invalid inputs
- Code passes type checking (mypy)
- Generated entirely via Claude Code from specifications

**Prohibited:**
- Manual code writing
- Undefined behavior
- Unvalidated inputs
- Mixing concerns (UI in data layer)

---

## PHASE II — Full-Stack Web Application with Authentication

### 4.2.1 Phase Objective
Transform console app into a production-grade, multi-user web application with persistent storage and stateless JWT authentication.

### 4.2.2 Mandatory Requirements

**Technology Stack:**
- **Frontend:** Next.js 15+ (App Router), TypeScript 5.7+, Tailwind CSS
- **Backend:** FastAPI 0.115+, SQLModel 0.0.22+
- **Database:** Neon Serverless PostgreSQL 16+
- **Authentication:** Better Auth 1.0+ with JWT
- **Package Management:** UV (backend), npm/pnpm (frontend)

**Architecture:**
- Monorepo structure:
  ```
  /frontend — Next.js application
  /backend — FastAPI application
  /specs — Specification files
  CLAUDE.md — Agent instructions
  AGENTS.md — Workflow definitions
  docker-compose.yml — Local development
  ```

**API Requirements:**
- RESTful endpoints under `/api/{user_id}/tasks`
- JWT authentication on all endpoints except `/health`
- User isolation enforced at query level
- OpenAPI documentation auto-generated
- CORS configured for frontend origin

**Required Endpoints:**
```
GET    /api/{user_id}/tasks          — List user's tasks
POST   /api/{user_id}/tasks          — Create task
GET    /api/{user_id}/tasks/{id}     — Get task details
PUT    /api/{user_id}/tasks/{id}     — Update task
DELETE /api/{user_id}/tasks/{id}     — Delete task
PATCH  /api/{user_id}/tasks/{id}/complete — Toggle completion
```

**Authentication Flow:**
1. User signs up/signs in via Better Auth
2. Better Auth issues JWT token
3. Frontend stores token securely (httpOnly cookie preferred)
4. Frontend includes token in `Authorization: Bearer <token>` header
5. Backend validates JWT signature using shared secret
6. Backend extracts `user_id` from token
7. Backend matches token `user_id` with URL `user_id`
8. Backend filters all queries by authenticated `user_id`

**Security Requirements:**
- JWT secret MUST be strong (256+ bits) and environment-based
- Token expiration MUST be set (7 days max)
- Backend MUST verify token signature on every request
- Backend MUST enforce user_id matching (token vs URL)
- Database queries MUST filter by authenticated user_id
- No user may access another user's tasks

**Database Schema:**
```sql
-- Managed by Better Auth
CREATE TABLE users (
  id TEXT PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Application data
CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL CHECK (length(title) >= 1 AND length(title) <= 200),
  description TEXT CHECK (length(description) <= 1000),
  completed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

**Frontend Requirements:**
- Server components by default
- Client components only for interactivity
- Centralized API client (`/lib/api.ts`)
- Environment variables for backend URL
- Loading states and error handling
- Responsive design (mobile-first)

**Quality Standards:**
- Frontend and backend fully typed
- API contracts defined in specs before implementation
- Integration tests for authentication flow
- E2E test for critical user journey (signup → create task → logout)

**Deliverables:**
- Updated `/specs` with Phase II specifications
- `/frontend` with Next.js application
- `/backend` with FastAPI application
- Database migration scripts (Alembic)
- `docker-compose.yml` for local development
- Updated `README.md` with Phase II setup
- Deployed frontend (Vercel) and backend URLs

**Acceptance Criteria:**
- User can sign up and log in
- JWT authentication works end-to-end
- User isolation is enforced (cannot see others' tasks)
- All Phase I features work via web UI
- API documentation is auto-generated and accessible
- Application is deployed and publicly accessible

**Prohibited:**
- Storing JWT in localStorage (XSS vulnerability)
- Hardcoded JWT secrets
- Missing user_id validation
- Shared database queries across users
- Manual SQL queries (use SQLModel ORM)

---

## PHASE III — AI-Powered Chatbot with MCP Architecture

### 4.3.1 Phase Objective
Create a conversational AI interface for task management using stateless architecture, MCP tools, and persistent conversation history.

### 4.3.2 Mandatory Requirements

**Technology Stack:**
- **Frontend:** OpenAI ChatKit (hosted or self-hosted)
- **Backend:** FastAPI + OpenAI Agents SDK + Official MCP SDK
- **Database:** Neon PostgreSQL (extended schema)
- **Authentication:** JWT (continued from Phase II)

**Architecture:**
```
ChatKit UI → FastAPI /api/chat endpoint → OpenAI Agent → MCP Tools → Database
                                              ↓
                                    Conversation stored in DB
```

**MCP Tools Specification:**

All tools MUST:
- Be stateless (no in-memory state)
- Accept `user_id` as first parameter
- Return structured JSON responses
- Handle errors gracefully
- Log all operations with correlation IDs

Required MCP Tools:
1. **add_task**
   - Parameters: `user_id` (str), `title` (str), `description` (str, optional)
   - Returns: `{task_id, status, title}`

2. **list_tasks**
   - Parameters: `user_id` (str), `status` (str, optional: "all"|"pending"|"completed")
   - Returns: Array of task objects

3. **complete_task**
   - Parameters: `user_id` (str), `task_id` (int)
   - Returns: `{task_id, status, title}`

4. **delete_task**
   - Parameters: `user_id` (str), `task_id` (int)
   - Returns: `{task_id, status, title}`

5. **update_task**
   - Parameters: `user_id` (str), `task_id` (int), `title` (str, optional), `description` (str, optional)
   - Returns: `{task_id, status, title}`

**Database Schema Extensions:**
```sql
CREATE TABLE conversations (
  id SERIAL PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE messages (
  id SERIAL PRIMARY KEY,
  conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
  content TEXT NOT NULL,
  tool_calls JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation ON messages(conversation_id);
```

**Stateless Conversation Flow:**
1. Client sends message + optional `conversation_id`
2. Backend fetches conversation history from database
3. Backend builds message array: history + new message
4. Backend stores user message in database
5. Backend invokes Agent with full history
6. Agent uses MCP tools (stateless, database-backed)
7. Backend stores assistant response in database
8. Backend returns response to client
9. **Server holds NO state** — ready for next request

**Agent Behavior Requirements:**
- Understand natural language commands (see Section 4.3.3)
- Always confirm actions ("I've created task 'Buy groceries'")
- Handle ambiguity by asking clarifying questions
- Gracefully handle errors ("Task 42 not found. Would you like to see all tasks?")
- Never invent task IDs — always query first

**Natural Language Command Examples:**
| User Says | Agent Action |
|-----------|--------------|
| "Add a task to buy groceries" | `add_task(title="Buy groceries")` |
| "Show me all my tasks" | `list_tasks(status="all")` |
| "Mark task 3 as done" | `complete_task(task_id=3)` |
| "Delete the meeting task" | `list_tasks()` → find ID → `delete_task()` |
| "Change task 1 to 'Call mom tonight'" | `update_task(task_id=1, title="Call mom tonight")` |

**Security Requirements:**
- All MCP tools MUST validate `user_id` against authenticated user
- Tools MUST NOT accept arbitrary `user_id` from AI
- Backend MUST enforce that token `user_id` matches tool calls
- AI MUST NOT have direct database access

**Quality Standards:**
- MCP tools have explicit input/output schemas
- Conversation history is complete and ordered
- AI responses are auditable (log tool calls)
- System recovers gracefully from AI errors
- Conversation can be resumed after server restart

**Deliverables:**
- `/specs` updated with chatbot specifications
- MCP server implementation (Python)
- ChatKit frontend integration
- Updated database migrations
- Agent prompt engineering documentation
- Deployed chatbot URL

**Acceptance Criteria:**
- User can manage tasks via natural language
- Conversation history persists across sessions
- MCP tools work correctly and securely
- AI cannot access other users' data
- System is stateless (survives server restarts)

**Prohibited:**
- AI with direct database access
- Stateful agent memory (must use database)
- Missing user_id validation in tools
- Exposing internal tool names to users

---

## PHASE IV — Local Kubernetes Deployment with Helm

### 4.4.1 Phase Objective
Containerize and deploy the application on local Kubernetes (Minikube) using Helm charts, demonstrating cloud-native patterns and AIOps.

### 4.4.2 Mandatory Requirements

**Technology Stack:**
- Docker 27+ (Docker Desktop)
- Docker AI Agent (Gordon) — for AI-assisted Docker operations
- Kubernetes 1.31+ (Minikube)
- Helm 3.16+
- kubectl-ai and/or Kagent — for AI-assisted K8s operations

**Architecture:**
```
┌─────────────────────────────────────────────┐
│ Minikube Cluster                            │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ Frontend │  │ Backend  │  │ MCP      │ │
│  │ Pod      │  │ Pod      │  │ Server   │ │
│  └──────────┘  └──────────┘  └──────────┘ │
│       │              │              │       │
│       └──────────────┴──────────────┘       │
│                     │                       │
│              ┌──────▼──────┐               │
│              │   Ingress    │               │
│              └──────────────┘               │
└─────────────────────────────────────────────┘
         │
    External DB (Neon)
```

**Containerization Requirements:**

Use Docker AI (Gordon) to generate Dockerfiles:
```bash
docker ai "Create a production Dockerfile for a Next.js 15 app with multi-stage build"
docker ai "Create a production Dockerfile for a FastAPI app with UV package manager"
```

**Dockerfile Standards:**
- Multi-stage builds for minimal image size
- Non-root user for security
- Health checks included
- Environment variables for configuration
- Layer caching optimization
- No secrets in images

**Helm Chart Structure:**
```
helm/
├── Chart.yaml
├── values.yaml
├── values-dev.yaml
├── values-prod.yaml
└── templates/
    ├── frontend-deployment.yaml
    ├── frontend-service.yaml
    ├── backend-deployment.yaml
    ├── backend-service.yaml
    ├── mcp-deployment.yaml
    ├── mcp-service.yaml
    ├── ingress.yaml
    ├── configmap.yaml
    └── secrets.yaml
```

**Kubernetes Resource Requirements:**

All deployments MUST include:
- Resource limits and requests
- Liveness and readiness probes
- Rolling update strategy
- Pod anti-affinity (for high availability)
- ConfigMaps for configuration
- Secrets for sensitive data

**Example Deployment (use kubectl-ai to generate):**
```bash
kubectl-ai "Create a deployment for frontend with 2 replicas, resource limits, and health checks"
kubectl-ai "Create a service for backend with ClusterIP and port 8000"
```

**AIOps Integration:**

Use kubectl-ai and Kagent:
```bash
# Deployment
kubectl-ai "deploy the todo frontend with 2 replicas and load balancer"

# Debugging
kubectl-ai "why are the backend pods failing?"
kubectl-ai "check logs for pods with label app=backend"

# Scaling
kubectl-ai "scale backend to 3 replicas to handle more load"

# Optimization
kagent "analyze cluster resource usage and suggest optimizations"
kagent "check if any pods are under-resourced"
```

**Health Checks:**
- Liveness probe: `/health`
- Readiness probe: `/health/ready` (checks DB connectivity)
- Initial delay: 10s
- Period: 10s
- Failure threshold: 3

**Observability:**
- All pods must emit structured logs to stdout
- Logs must include correlation IDs
- Use `kubectl logs` for debugging
- Consider logging aggregation (future enhancement)

**Local Development Workflow:**
1. Start Minikube: `minikube start --cpus=4 --memory=8192`
2. Build images: `docker build -t frontend:local ./frontend`
3. Load images: `minikube image load frontend:local`
4. Install Helm chart: `helm install taskflow ./helm -f values-dev.yaml`
5. Expose service: `minikube service frontend --url`

**Quality Standards:**
- All Kubernetes manifests generated via kubectl-ai/specs
- Helm values.yaml documented with comments
- Images scanned for vulnerabilities
- Resource limits prevent resource exhaustion
- Graceful shutdown handling (SIGTERM)

**Deliverables:**
- Dockerfiles for all services
- Helm chart with full configuration
- `README-k8s.md` with deployment instructions
- Health check endpoints implemented
- Updated specs for infrastructure

**Acceptance Criteria:**
- Application runs on Minikube
- All pods healthy and ready
- Services communicate correctly
- Ingress routes traffic properly
- Application survives pod restarts
- kubectl-ai successfully deploys from specs

**Prohibited:**
- Hardcoded IPs or hostnames
- Missing health checks
- Unlimited resource requests
- Secrets in ConfigMaps
- Manual kubectl without specs

---

## PHASE V — Advanced Cloud Deployment with Event-Driven Architecture

### 4.5.1 Phase Objective
Deploy production-grade system on cloud Kubernetes with advanced features (recurring tasks, reminders), event-driven architecture (Kafka), and distributed runtime (Dapr).

### 4.5.2 Mandatory Requirements

**Technology Stack:**
- **Cloud:** Azure AKS / Google Cloud GKE / Oracle OKE
- **Kubernetes:** 1.31+
- **Helm:** 3.16+
- **Event Streaming:** Kafka 3.9+ or Redpanda Cloud
- **Distributed Runtime:** Dapr 1.14+
- **CI/CD:** GitHub Actions

**Part A: Advanced Features**

Implement all Advanced and Intermediate features:
- **Intermediate:** Priorities (High/Medium/Low), Tags/Categories, Search & Filter, Sort
- **Advanced:** Recurring Tasks, Due Dates & Reminders

**Database Schema Extensions:**
```sql
ALTER TABLE tasks ADD COLUMN priority TEXT CHECK (priority IN ('high', 'medium', 'low')) DEFAULT 'medium';
ALTER TABLE tasks ADD COLUMN tags TEXT[] DEFAULT '{}';
ALTER TABLE tasks ADD COLUMN due_date TIMESTAMP;
ALTER TABLE tasks ADD COLUMN recurrence_rule TEXT; -- cron or ISO 8601
ALTER TABLE tasks ADD COLUMN parent_task_id INTEGER REFERENCES tasks(id);

CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_tags ON tasks USING gin(tags);
```

**Part B: Event-Driven Architecture**

**Kafka Topics:**
```
task-events      — All CRUD operations (producer: MCP tools)
reminders        — Scheduled reminders (producer: task creation, consumer: notification service)
task-updates     — Real-time sync (producer: all services, consumer: WebSocket service)
recurring-tasks  — Recurring task triggers (producer: completion, consumer: recurring service)
```

**Event Schema (task-events):**
```json
{
  "event_id": "uuid",
  "event_type": "created|updated|completed|deleted",
  "task_id": 123,
  "user_id": "user_abc",
  "task_data": {...},
  "timestamp": "2026-01-05T12:00:00Z",
  "correlation_id": "uuid"
}
```

**New Microservices:**
1. **Notification Service**
   - Consumes: `reminders` topic
   - Action: Sends push notifications / emails
   - Stack: FastAPI + async Kafka consumer

2. **Recurring Task Service**
   - Consumes: `recurring-tasks` topic
   - Action: Creates next task occurrence
   - Logic: Parses recurrence rule, creates new task

3. **Audit Service** (optional bonus)
   - Consumes: `task-events` topic
   - Action: Stores complete audit log
   - Storage: Separate audit database/table

**Part C: Dapr Integration**

**Dapr Building Blocks:**
1. **Pub/Sub:** Abstract Kafka interactions
2. **State Management:** Conversation state (alternative to direct DB)
3. **Service Invocation:** Service-to-service calls with retries
4. **Jobs API:** Schedule exact-time reminders (better than cron polling)
5. **Secrets Management:** Store API keys securely

**Dapr Components:**

`kafka-pubsub.yaml`:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "kafka-cluster:9092"
    - name: consumerGroup
      value: "taskflow-group"
```

`statestore.yaml`:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.postgresql
  version: v1
  metadata:
    - name: connectionString
      secretKeyRef:
        name: db-connection
        key: connection-string
```

**Dapr Jobs API Usage (Reminders):**
```python
# Schedule reminder at exact time
await httpx.post(
    f"http://localhost:3500/v1.0-alpha1/jobs/reminder-task-{task_id}",
    json={
        "dueTime": remind_at.isoformat(),
        "data": {"task_id": task_id, "user_id": user_id}
    }
)

# Handle callback when job fires
@app.post("/api/jobs/trigger")
async def handle_job_trigger(request: Request):
    job_data = await request.json()
    # Publish to notification service via Dapr PubSub
    await publish_event("reminders", job_data["data"])
    return {"status": "SUCCESS"}
```

**Part D: Cloud Deployment**

**Cloud Provider Setup:**
- **Azure AKS:** Use $200 free credit
- **Google GKE:** Use $300 credit for 90 days
- **Oracle OKE:** Use Always Free tier (recommended for no time pressure)

**Deployment Architecture:**
```
┌─────────────────────────────────────────────────────┐
│ Cloud Kubernetes Cluster (AKS/GKE/OKE)            │
│                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Frontend │  │ Backend  │  │ Notif    │        │
│  │ + Dapr   │  │ + Dapr   │  │ Service  │        │
│  └──────────┘  └──────────┘  │ + Dapr   │        │
│                               └──────────┘        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ MCP      │  │ Recurring│  │ Audit    │        │
│  │ + Dapr   │  │ Service  │  │ Service  │        │
│  └──────────┘  └──────────┘  └──────────┘        │
│         │              │              │            │
│         └──────────────┴──────────────┘            │
│                     │                              │
│              ┌──────▼──────┐                      │
│              │   Ingress    │                      │
└─────────────────────────────────────────────────────┘
         │
    External Services (Neon DB, Kafka, etc.)
```

**Quality Standards:**
- All microservices stateless with Dapr sidecars
- Event schema versioned and documented
- At-least-once delivery semantics for events
- Idempotent consumers
- Complete observability across event flows

**Deliverables:**
- Updated `/specs` with Phase V specifications
- Advanced features implemented and tested
- Kafka topics configured and documented
- Notification service deployed
- Recurring task service deployed
- Dapr components configured
- Cloud deployment running
- CI/CD pipeline configured
- Updated deployment documentation

**Acceptance Criteria:**
- Advanced features (priorities, tags, recurring tasks) work end-to-end
- Event-driven architecture operational
- Kafka events flowing correctly
- Dapr services communicating
- Notifications sent for reminders
- Recurring tasks create next occurrence
- System deployed on cloud Kubernetes
- CI/CD pipeline functional

**Prohibited:**
- Missing user_id validation in any service
- Secrets in ConfigMaps
- Manual kubectl without specs
- Stateful microservices
- Non-idempotent event consumers

---

## Response snapshot

Successfully created the TaskFlow AI Constitution at `.specify/memory/constitution.md` with the following structure:

- **Version 1.0.0** with 5 Core Principles:
  1. Spec-First Development
  2. AI as Controlled Executor
  3. Determinism and Reproducibility
  4. Production-Grade Standards
  5. Stateless Architecture Priority

- **Global Quality Standards** covering:
  - Specification, Implementation, Security, Technology Baseline
  - Code Quality, Observability

- **Phase-Specific Constraints** for all 5 phases:
  - Phase I: In-Memory Python Console
  - Phase II: Full-Stack Web App with JWT Auth
  - Phase III: AI Chatbot with MCP
  - Phase IV: Kubernetes Deployment with Helm
  - Phase V: Cloud Deployment with Event-Driven Architecture (Kafka, Dapr)

- **Governance** section with amendment process, versioning policy, and compliance review

All templates are compatible with no updates required.

## Outcome

- ✅ Impact: Initial project constitution created, establishing quality standards for all phases
- 🧪 Tests: N/A (constitution only)
- 📁 Files: `.specify/memory/constitution.md` created
- 🔁 Next prompts: Consider creating feature specifications for Phase I
- 🧠 Reflection: Constitution provides comprehensive governance aligned with the user input for TaskFlow AI project across 5 phases

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
