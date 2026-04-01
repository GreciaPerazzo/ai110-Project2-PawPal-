import pytest
from datetime import date, time, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


def test_task_completion():
    """Test that calling mark_complete() on a Task changes its completed status to True."""
    # Create a sample pet for the task
    pet = Pet(name="TestPet", breed="TestBreed", species="TestSpecies", age=1)

    # Create a task
    task = Task(
        task_type="Test Task",
        date=date.today(),
        time=time(12, 0),
        pet=pet,
        notes="Test notes"
    )

    # Initially, task should not be completed
    assert not task.completed
    assert not task.is_completed()

    # Mark the task as complete
    task.mark_complete()

    # Now the task should be completed
    assert task.completed
    assert task.is_completed()


def test_task_addition():
    """Test that adding a task to a Pet increases that pet's task count by 1."""
    # Create a pet
    pet = Pet(name="TestPet", breed="TestBreed", species="TestSpecies", age=1)

    # Initially, pet should have no tasks
    assert len(pet.tasks) == 0
    assert len(pet.get_tasks()) == 0

    # Create a task
    task = Task(
        task_type="Test Task",
        date=date.today(),
        time=time(12, 0),
        pet=pet,
        notes="Test notes"
    )

    # Add the task to the pet
    pet.add_task(task)

    # Now the pet should have 1 task
    assert len(pet.tasks) == 1
    assert len(pet.get_tasks()) == 1
    assert task in pet.tasks


def test_sort_by_time():
    """Test that sort_by_time() returns tasks in chronological order."""
    # Create owner and pet
    owner = Owner("TestOwner")
    pet = Pet(name="Buddy", breed="Golden", species="Dog", age=3)
    owner.add_pet(pet)

    today = date.today()

    # Create tasks OUT OF ORDER
    task_evening = Task(
        task_type="Play",
        date=today,
        time=time(18, 0),  # 6:00 PM
        pet=pet,
        notes="Evening play"
    )
    task_morning = Task(
        task_type="Walk",
        date=today,
        time=time(8, 0),  # 8:00 AM
        pet=pet,
        notes="Morning walk"
    )
    task_afternoon = Task(
        task_type="Feeding",
        date=today,
        time=time(12, 0),  # 12:00 PM
        pet=pet,
        notes="Lunch"
    )

    # Add tasks in random order
    pet.add_task(task_evening)
    pet.add_task(task_morning)
    pet.add_task(task_afternoon)

    # Create scheduler
    scheduler = Scheduler(owner)

    # Sort tasks by time
    sorted_tasks = scheduler.sort_by_time()

    # Verify they are in chronological order
    assert len(sorted_tasks) == 3
    assert sorted_tasks[0].time == time(8, 0)   # Morning
    assert sorted_tasks[1].time == time(12, 0)  # Afternoon
    assert sorted_tasks[2].time == time(18, 0)  # Evening

    # Verify task types are in correct order
    assert sorted_tasks[0].task_type == "Walk"
    assert sorted_tasks[1].task_type == "Feeding"
    assert sorted_tasks[2].task_type == "Play"


def test_recurrence_logic():
    """Test that marking a daily task complete creates a new task for tomorrow."""
    # Create owner and pet
    owner = Owner("TestOwner")
    pet = Pet(name="Luna", breed="Siamese", species="Cat", age=2)
    owner.add_pet(pet)

    today = date.today()
    tomorrow = today + timedelta(days=1)

    # Create a daily task
    daily_task = Task(
        task_type="Medication",
        date=today,
        time=time(9, 0),  # 9:00 AM
        pet=pet,
        notes="Daily meds",
        frequency="daily"
    )

    pet.add_task(daily_task)

    # Verify initial state
    assert len(pet.get_tasks()) == 1
    assert not daily_task.completed
    assert daily_task.frequency == "daily"

    # Mark the task as complete
    daily_task.mark_complete()

    # Verify original task is marked complete
    assert daily_task.completed

    # Verify a new task was created for tomorrow
    assert len(pet.get_tasks()) == 2

    # Find the new task (the one not yet completed)
    pending_tasks = pet.get_pending_tasks()
    assert len(pending_tasks) == 1

    new_task = pending_tasks[0]
    assert new_task.date == tomorrow
    assert new_task.time == time(9, 0)
    assert new_task.task_type == "Medication"
    assert new_task.frequency == "daily"
    assert new_task.notes == "Daily meds"
    assert not new_task.completed


def test_conflict_detection():
    """Test that detect_conflicts() identifies two tasks scheduled at the same time."""
    # Create owner and pet
    owner = Owner("TestOwner")
    pet = Pet(name="Buddy", breed="Golden", species="Dog", age=3)
    owner.add_pet(pet)

    today = date.today()

    # Create two tasks at the SAME time (conflict)
    conflict_task1 = Task(
        task_type="Vet Appointment",
        date=today,
        time=time(14, 0),  # 2:00 PM
        pet=pet,
        notes="Annual checkup"
    )
    conflict_task2 = Task(
        task_type="Training Session",
        date=today,
        time=time(14, 0),  # 2:00 PM (SAME TIME!)
        pet=pet,
        notes="Obedience training"
    )

    pet.add_task(conflict_task1)
    pet.add_task(conflict_task2)

    # Create scheduler
    scheduler = Scheduler(owner)

    # Detect conflicts
    conflict_message = scheduler.detect_conflicts()

    # Verify conflict was detected
    assert "SCHEDULING CONFLICTS DETECTED" in conflict_message
    assert "Buddy" in conflict_message
    assert "2 tasks" in conflict_message
    assert "Vet Appointment" in conflict_message
    assert "Training Session" in conflict_message
    assert "14:00" in conflict_message or "2:00 PM" in conflict_message or "14:00:00" in conflict_message
