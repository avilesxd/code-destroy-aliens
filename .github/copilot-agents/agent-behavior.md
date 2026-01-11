# Agent Behavior Guidelines

## When to Ask vs. Act

### Execute Directly

Simple, well-defined tasks that are clear and straightforward:

- "add a new bullet color"
- "fix typo in docstring"
- "update version number"
- "add a new constant to configuration"
- "rename a variable for clarity"

### Confirm Understanding First

Complex changes that could affect multiple parts of the system:

- "refactor collision system"
- "add new game mode"
- "architectural changes"
- "change entity creation pattern"
- "modify game loop structure"

### Ask Specific Questions

Unclear requirements or missing information:

- **Never assume implicit requirements**
- Ask about asset paths, configuration values, behavior edge cases
- Request clarification rather than guessing
- Verify expected behavior for edge cases

## Before Making Changes

### 1. Verify Context

Read relevant files to understand current implementation:

- Check the file you're modifying
- Review related files in the same module
- Understand data flow and dependencies

### 2. Check Dependencies

Look for usages with `list_code_usages` if modifying shared code:

```
If changing a function signature, check all call sites
If modifying a class, check all instantiation points
If renaming, verify all imports
```

### 3. Run Verification

Execute `npm run verify` before claiming task complete:

- This runs: format → prettier → lint → typecheck → test
- All checks must pass
- No exceptions

### 4. Update Tests

Add/modify tests when changing behavior, **even if not explicitly requested**:

- New features need new tests
- Bug fixes need regression tests
- Refactors should maintain test coverage

## Quality Standards (Non-Negotiable)

### Code Requirements

- ✅ No type errors (`npm run typecheck` must pass)
- ✅ No linting violations (`npm run lint` must pass)
- ✅ No failing tests (`npm run test` must pass)
- ✅ Code must be formatted (`npm run format`)
- ✅ Docstrings for new classes and public methods

### Before Every Commit

```bash
# Run these in order (or use npm run verify)
npm run lint        # Fix linting issues
npm run typecheck   # Fix type errors
npm run test        # Verify tests pass
npm run format      # Auto-format code
```

### Zero Tolerance Policy

**No code is accepted with**:

- Type errors
- Linting violations
- Failing tests
- Missing type annotations on new functions
- Unformatted code

## Performance Decisions

### Don't Guess - Measure

Never assume performance characteristics:

- Don't guess about speed, memory usage, or bundle size
- Don't optimize prematurely
- Don't assume "X is slow" without proof

### Add Instrumentation First

Before optimizing, add measurement:

- Timing decorators for functions
- Frame rate counters for rendering
- Memory profiling for large data structures
- Actual profiling with `cProfile`

Example:

```python
import time

def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

@measure_time
def update_aliens(game: Game) -> None:
    # ... implementation
```

### Test in Isolation

- Validate changes in small scope before applying project-wide
- Test with representative data/scenarios
- Check FPS counter after rendering changes
- Profile before/after optimization

## Communication Guidelines

### Be Specific

When asking questions or reporting status:

- ✅ "Type error in `src/entities/ship.py` line 45: `ship.x` expects float, got
  int"
- ❌ "There's a type error somewhere"

### Explain Changes

When making complex changes:

- What changed
- Why it changed
- How it was verified
- Any side effects or breaking changes

### Report Progress

For multi-step tasks:

- List what's completed
- List what remains
- Note any blockers or issues
- Ask for clarification if needed

## Handling Uncertainty

### Technical Uncertainty

If you're unsure about:

- Architecture decisions → Ask before implementing
- Breaking changes → Confirm with user
- Performance implications → Measure before optimizing
- Type signatures → Review existing patterns

### Requirement Uncertainty

If requirements are unclear:

- Don't assume implicit requirements
- Ask specific questions
- Provide options with trade-offs
- Request examples or use cases

### Missing Information

If information is missing:

- Asset paths → Ask for confirmation
- Configuration values → Request expected values
- Behavior edge cases → Ask what should happen
- Test data → Request representative examples

## Documenting New Constraints

### When to Document

If introducing a new rule like:

- "Always X" (e.g., "Always use resource_path() for assets")
- "Never Y" (e.g., "Never instantiate entities directly")
- New patterns or conventions
- Architecture decisions

### Where to Document

1. **conventions.md** for code standards
2. **architecture.md** for architectural patterns
3. **workflows.md** for development processes
4. Update main **copilot-instructions.md** with cross-reference

### Documentation Format

````markdown
## New Convention: [Name]

**Rule**: [Clear statement of the rule]

**Rationale**: [Why this rule exists]

**Example**:

```python
# ✅ Good
[correct example]

# ❌ Bad
[incorrect example]
```
````

**Related**: [Links to related documentation]

```

## Error Handling

### When Tests Fail
1. Read the error message carefully
2. Check recent changes that might have caused it
3. Run the specific failing test in isolation
4. Fix the underlying issue (don't just update the test)
5. Verify the fix with `npm run test`

### When Type Checking Fails
1. Read mypy output for specific errors
2. Fix type annotations (don't use `# type: ignore` unless absolutely necessary)
3. Ensure all function signatures are typed
4. Run `npm run typecheck` to verify

### When Linting Fails
1. Review flake8 output
2. Fix issues (don't disable rules without justification)
3. Run `npm run format` to auto-fix formatting
4. Run `npm run lint` to verify

## Best Practices

### Code Reviews
Before submitting changes:
- Review your own changes first
- Run `npm run verify` to catch issues
- Check for unintended modifications
- Verify tests cover new behavior

### Incremental Changes
- Make small, focused changes
- Commit frequently with meaningful messages
- Test after each logical change
- Don't mix unrelated changes

### Learning from Codebase
- Study existing patterns before implementing new features
- Look at similar entities/functions for reference
- Follow established naming conventions
- Maintain consistency with existing code style

## Quick Reference Checklist

Before claiming a task is complete:

- [ ] Code compiles and runs without errors
- [ ] All type hints are present and correct
- [ ] Code passes `npm run lint`
- [ ] Code passes `npm run typecheck`
- [ ] All tests pass (`npm run test`)
- [ ] New/updated tests cover changes
- [ ] Code is formatted (`npm run format`)
- [ ] Docstrings added for new classes/methods
- [ ] No hardcoded values (use configuration)
- [ ] Asset loading uses `resource_path()`
- [ ] Commit message follows conventions
- [ ] Changes are documented if introducing new patterns
```
