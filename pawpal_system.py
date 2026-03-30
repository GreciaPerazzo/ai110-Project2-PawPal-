from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, time
from typing import List


@dataclass
class Pet:
    name: str
    breed: str
    species: str
    age: int


@dataclass
class Task:
    task_type: str  # e.g., walk, feeding, medication, grooming, vet appointment
    date: date
    time: time
    pet: Pet 
    notes: str = ""
    

class Owner:
    def __init__(self, name: str):
        self.name: str = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet: Pet) -> None:
        pass


class Scheduler:
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def get_todays_tasks(self) -> List[Task]:
        pass

    def send_reminders(self) -> None:
        pass
