import pytest
from datetime import date, time
from pawpal_system import Task, Pet


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
