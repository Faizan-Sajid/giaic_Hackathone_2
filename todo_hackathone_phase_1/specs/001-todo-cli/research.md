# Research: Todo Console App Architecture

**Date**: 2025-12-31
**Feature**: 001-todo-cli
**Status**: Complete

## Technical Decisions

### 1. Language: Python 3.13+

**Decision**: Python 3.13+ standard library only

**Rationale**:
- Constitution explicitly requires Python 3.13+
- Standard library provides all needed features (argparse, dataclasses, typing)
- No external dependencies simplifies deployment and testing
- Cross-platform compatibility built-in

**Alternatives Considered**:
- Python 3.12: Does not meet constitution requirement
- External CLI framework (Click, Typer): Adds unnecessary complexity

### 2. In-Memory Storage Strategy

**Decision**: Python list with integer ID counter

**Rationale**:
- Simple list provides O(1) append and O(n) linear search
- Integer ID counter ensures unique, deterministic IDs
- No persistence required by constitution
- Easy to test and reason about

**Alternatives Considered**:
- Dictionary: Slightly faster lookups but list is sufficient for <1000 items
- Set: Loses order information needed for consistent display

### 3. Clean Architecture Layering

**Decision**: Four-layer architecture (Model, Repository, Service, CLI)

**Rationale**:
- Follows constitution principle VI: Separation of concerns
- Each layer has single responsibility
- Enables independent testing of each layer
- Future-proofs for potential Phase II enhancements

**Layer Responsibilities**:
- **Model**: Pure data representation (Task dataclass)
- **Repository**: Storage operations and ID generation
- **Service**: Business logic and validation
- **CLI**: User interaction and output formatting

### 4. CLI Interaction Pattern

**Decision**: Numbered menu with numeric input

**Rationale**:
- User input specifies numbered options (1-6)
- Simple to implement with Python's input()
- Consistent with constitution requirement for explicit CLI
- Easy to extend with additional menu options

**Menu Structure**:
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Completion
6. Exit

## Best Practices Applied

### Input Validation
- All user input validated before processing
- Empty titles rejected with clear error messages
- Invalid numeric input handled gracefully

### Error Handling
- TaskNotFoundError for missing IDs
- EmptyTitleError for validation failures
- InvalidInputError for malformed input
- All errors display user-friendly messages (no stack traces)

### ID Generation Strategy
- Start at 1, increment for each new task
- Unique within session (not globally)
- Never reused even after task deletion

## Conclusion

The architecture is well-suited for Phase I requirements. All decisions align with constitution principles. No further research needed.
