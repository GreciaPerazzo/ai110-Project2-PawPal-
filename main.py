from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date, time

def main():
    # Create Owner
    owner = Owner("Alex")

    # Create pets
    buddy = Pet(name="Buddy", breed="Golden Retriever", species="Dog", age=3)
    luna = Pet(name="Luna", breed="Siamese", species="Cat", age=2)

    # Get today's date
    today = date.today()

    # Create tasks for Buddy
    walk_task = Task(
        task_type="Walk",
        date=today,
        time=time(8, 0),  # 8:00 AM
        pet=buddy,
        notes="30-minute walk in the park"
    )
    feeding_task = Task(
        task_type="Feeding",
        date=today,
        time=time(12, 0),  # 12:00 PM
        pet=buddy,
        notes="Morning feeding - 1 cup of kibble"
    )

    # Create tasks for Luna
    medication_task = Task(
        task_type="Medication",
        date=today,
        time=time(9, 0),  # 9:00 AM
        pet=luna,
        notes="Flea treatment - apply topically"
    )
    play_task = Task(
        task_type="Play Time",
        date=today,
        time=time(18, 0),  # 6:00 PM
        pet=luna,
        notes="Interactive play with laser pointer"
    )

    # Add tasks to pets
    buddy.add_task(walk_task)
    buddy.add_task(feeding_task)
    luna.add_task(medication_task)
    luna.add_task(play_task)

    # Add pets to owner
    owner.add_pet(buddy)
    owner.add_pet(luna)

    # Create Scheduler
    scheduler = Scheduler(owner)

    # Print Today's Schedule
    print("=== Today's Schedule for Alex ===")
    todays_tasks = scheduler.get_todays_tasks()

    if not todays_tasks:
        print("No tasks scheduled for today.")
        return

    # Sort tasks by time
    todays_tasks.sort(key=lambda t: t.time)

    for task in todays_tasks:
        status = "✓" if task.completed else "○"
        print(f"{status} {task.time.strftime('%I:%M %p')} - {task.task_type} for {task.pet.name} ({task.pet.species})")
        if task.notes:
            print(f"    Notes: {task.notes}")
        print()
if __name__ == "__main__":
    main()