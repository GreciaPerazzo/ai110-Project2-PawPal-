# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling Features

PawPal+ now includes powerful scheduling utilities to help pet owners organize and manage tasks efficiently:

### 1. **Task Sorting**
Sort all tasks chronologically using the `sort_by_time()` method. Displays your pet care schedule in order from earliest to latest, making it easy to see what needs to happen first.

### 2. **Task Filtering**
Use `filter_tasks()` to narrow down your task list by:
- **Status**: View only pending tasks or completed tasks
- **Pet Name**: View all tasks for a specific pet
- **Combined**: Filter by both status and pet name for powerful scoping

Example: `scheduler.filter_tasks(status="pending", pet_name="Buddy")`

### 3. **Recurring Tasks**
Schedule tasks that automatically repeat. Set `frequency` to:
- **`"daily"`**: Task reschedules for tomorrow at the same time
- **`"weekly"`**: Task reschedules 7 days later at the same time
- **`"once"`**: One-time task (no automatic rescheduling)

When marked complete, daily/weekly tasks automatically create a new occurrence, ensuring you never miss a pattern.

### 4. **Conflict Detection**
The `detect_conflicts()` method scans your schedule and alerts you to double-bookings. It identifies when two or more tasks are scheduled for the same pet at the same date and time, helping prevent scheduling errors before they happen.

These features work together to keep your pet care routine organized, predictable, and conflict-free.

## Testing PawPal+

### Running Tests

Execute the test suite with:

```bash
python -m pytest tests/test_pawpal.py -v
```

### Test Coverage

The PawPal+ test suite includes **5 comprehensive tests** that validate core functionality:

1. **Task Completion** — Verifies that `mark_complete()` correctly updates task status
2. **Task Addition** — Confirms that tasks are properly added to a pet's task list
3. **Sorting Correctness** — Validates that `sort_by_time()` returns tasks in chronological order (morning → afternoon → evening)
4. **Recurrence Logic** — Tests that daily/weekly tasks automatically create next occurrences when marked complete, with correct date and time
5. **Conflict Detection** — Ensures `detect_conflicts()` correctly identifies and reports tasks scheduled at the same time for the same pet

### Test Confidence

**★★★★☆ 4 out of 5 stars**

The test suite covers critical happy-path scenarios and essential edge cases (empty states, sorting order, recurring task generation). Additional confidence would come from tests for cross-boundary date handling (month/year changes), extended recurring sequences, and more comprehensive filtering variations.
