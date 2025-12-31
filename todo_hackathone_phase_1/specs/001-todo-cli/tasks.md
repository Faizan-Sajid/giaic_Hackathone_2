---

description: "Task list template for feature implementation"
---

# Tasks: Todo Console App

**Input**: Design documents from `/specs/001-todo-cli/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are NOT included by default - tests must be explicitly requested.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Single project: `src/`, `tests/` at repository root
- Paths shown below assume single project structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan in src/models/, src/services/, src/repository/, src/cli/, and todo_app.py
- [x] T002 Add Task dataclass in src/models/task.py
- [x] T003 Implement TaskRepository in src/repository/task_repository.py with in-memory storage

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 [P] Implement TaskService in src/services/task_service.py (validation, business logic)
- [x] T005 [P] Implement CLI menu display in src/cli/menu.py (menu function, input parsing)
- [x] T006 [P] Implement main application loop in todo_app.py (menu flow, program lifecycle)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Core Task Management (Priority: P1) MVP

**Goal**: Users can add tasks and view the task list

**Independent Test**: Run app, add task with title, verify task appears in list with ID and pending status

### Implementation for User Story 1

- [x] T007 [P] [US1] Implement add_task workflow in src/cli/menu.py (menu option 1, input prompts, output)
- [x] T008 [P] [US1] Implement view_tasks workflow in src/cli/menu.py (menu option 2, empty state, list display)

**Checkpoint**: User Story 1 complete - users can add and view tasks independently

---

## Phase 4: User Story 2 - Task Modification (Priority: P2)

**Goal**: Users can update task details and toggle completion status

**Independent Test**: Add task, update title, toggle completion, verify changes persisted

### Implementation for User Story 2

- [x] T009 [P] [US2] Implement update_task workflow in src/cli/menu.py (menu option 3, ID input, field updates)
- [x] T010 [P] [US2] Implement toggle completion workflow in src/cli/menu.py (menu option 5, status flip)

**Checkpoint**: User Story 2 complete - users can modify tasks independently

---

## Phase 5: User Story 3 - Task Removal (Priority: P3)

**Goal**: Users can delete tasks they no longer need

**Independent Test**: Add task, delete it, verify it no longer appears in list

### Implementation for User Story 3

- [x] T011 [US3] Implement delete_task workflow in src/cli/menu.py (menu option 4, removal logic)

**Checkpoint**: User Story 3 complete - users can delete tasks independently

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T012 Implement input validation and error handling across all CLI operations (empty title, invalid ID, non-numeric input)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can proceed in parallel after Foundational complete
  - Or sequentially in priority order (P1 -> P2 -> P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational - May integrate with US1 but independently testable
- **User Story 3 (P3)**: Can start after Foundational - May integrate with US1/US2 but independently testable

### Within Each User Story

- Core implementation (model/service) before CLI integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel
- Models and services within a story marked [P] can run in parallel

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test adding and viewing tasks
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational -> Foundation ready
2. Add User Story 1 -> Test independently -> Deploy/Demo (MVP!)
3. Add User Story 2 -> Test independently -> Deploy/Demo
4. Add User Story 3 -> Test independently -> Deploy/Demo
5. Add Phase 6: Polish -> Final release

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Parallel Example: User Story 1

```bash
Task: "T007 [US1] Implement add_task workflow in src/cli/menu.py"
Task: "T008 [US1] Implement view_tasks workflow in src/cli/menu.py"
```

---

## Task Summary

| ID | Task | Phase | Story |
|----|------|-------|-------|
| T001 | Create project structure | Setup | - |
| T002 | Add Task dataclass | Setup | - |
| T003 | Implement TaskRepository | Setup | - |
| T004 | Implement TaskService | Foundational | - |
| T005 | Implement CLI menu display | Foundational | - |
| T006 | Implement main loop | Foundational | - |
| T007 | Implement add_task workflow | US1 | US1 |
| T008 | Implement view_tasks workflow | US1 | US1 |
| T009 | Implement update_task workflow | US2 | US2 |
| T010 | Implement toggle workflow | US2 | US2 |
| T011 | Implement delete_task workflow | US3 | US3 |
| T012 | Input validation & errors | Polish | - |

**Total Tasks**: 12
**User Story 1 Tasks**: 2
**User Story 2 Tasks**: 2
**User Story 3 Tasks**: 1
**Shared/Polish Tasks**: 7

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
