from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, time, datetime, timedelta
from typing import List


@dataclass
class Task:
    task_type: str  # e.g., walk, feeding, medication, grooming, vet appointment
    date: date
    time: time
    pet: Pet 
    notes: str = ""
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def is_completed(self) -> bool:
        """Return whether the task is completed."""
        return self.completed


@dataclass
class Pet:
    name: str
    breed: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the pet."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks for the pet."""
        return self.tasks

    def get_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks for the pet."""
        return [task for task in self.tasks if not task.completed]

    def get_completed_tasks(self) -> List[Task]:
        """Return all completed tasks for the pet."""
        return [task for task in self.tasks if task.completed]


class Owner:
    def __init__(self, name: str):
        """Initialize an owner with a name and empty pet list."""
        self.name: str = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        if pet not in self.pets:
            self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner's pet list."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_pets(self) -> List[Pet]:
        """Return all pets owned by the owner."""
        return self.pets

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks from all owned pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks from all owned pets."""
        return [task for task in self.get_all_tasks() if not task.completed]

    def get_tasks_for_pet(self, pet: Pet) -> List[Task]:
        """Return all tasks for a specific pet owned by the owner."""
        if pet in self.pets:
            return pet.tasks
        return []


class Scheduler:
    def __init__(self, owner: Owner):
        """Initialize a scheduler for an owner."""
        self.owner = owner
        self.tasks = owner.get_all_tasks()  # or manage separately?

    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler and its associated pet."""
        # Assuming tasks are added to pets, but scheduler can add directly?
        # For now, add to the pet's tasks
        task.pet.add_task(task)
        self.tasks = self.owner.get_all_tasks()  # refresh

    def remove_task(self, task: Task) -> None:
        """Remove a task from the scheduler and its associated pet."""
        task.pet.remove_task(task)
        self.tasks = self.owner.get_all_tasks()

    def get_todays_tasks(self) -> List[Task]:
        """Return all tasks scheduled for today."""
        today = datetime.today().date()
        return [task for task in self.tasks if task.date == today]

    def get_upcoming_tasks(self, days: int = 7) -> List[Task]:
        """Return all tasks within the specified number of days from today."""
        today = datetime.today().date()
        upcoming_date = today + timedelta(days=days)
        return [task for task in self.tasks if today <= task.date <= upcoming_date]

    def send_reminders(self) -> None:
        """Print reminders for all incomplete tasks scheduled for today."""
        todays_tasks = self.get_todays_tasks()
        if todays_tasks:
            print(f"Reminders for {self.owner.name}:")
            for task in todays_tasks:
                if not task.completed:
                    print(f"- {task.task_type} for {task.pet.name} at {task.time}")
        else:
            print(f"No tasks for today for {self.owner.name}.")

    def get_tasks_by_date(self, target_date: date) -> List[Task]:
        """Return all tasks scheduled for a specific date."""
        return [task for task in self.tasks if task.date == target_date]

    def get_overdue_tasks(self) -> List[Task]:
        """Return all incomplete tasks with dates before today."""
        today = datetime.today().date()
        return [task for task in self.tasks if task.date < today and not task.completed]
