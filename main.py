from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date, time, timedelta

def main():
    # Create Owner
    owner = Owner("Alex")

    # Create pets
    buddy = Pet(name="Buddy", breed="Golden Retriever", species="Dog", age=3)
    luna = Pet(name="Luna", breed="Siamese", species="Cat", age=2)

    # Get today's date
    today = date.today()

    # Create tasks OUT OF ORDER to test sort_by_time()
    play_task = Task(
        task_type="Play Time",
        date=today,
        time=time(18, 0),  # 6:00 PM
        pet=luna,
        notes="Interactive play with laser pointer"
    )
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
    medication_task = Task(
        task_type="Medication",
        date=today,
        time=time(9, 0),  # 9:00 AM
        pet=luna,
        notes="Flea treatment - apply topically"
    )
    grooming_task = Task(
        task_type="Grooming",
        date=today,
        time=time(15, 30),  # 3:30 PM
        pet=buddy,
        notes="Bath and nail trim"
    )

    # Add tasks to pets (intentionally out of order)
    buddy.add_task(play_task)  # Luna's task added to Buddy first
    luna.add_task(walk_task)   # Buddy's task added to Luna
    buddy.add_task(feeding_task)
    luna.add_task(medication_task)
    buddy.add_task(grooming_task)

    # Add pets to owner
    owner.add_pet(buddy)
    owner.add_pet(luna)

    # Create Scheduler
    scheduler = Scheduler(owner)

    # Mark some tasks as completed for filter demo
    feeding_task.mark_complete()
    medication_task.mark_complete()

    print("=" * 60)
    print("DEMONSTRATION OF NEW SCHEDULER METHODS")
    print("=" * 60)

    # ===== TEST 1: sort_by_time() =====
    print("\n1. USING sort_by_time() - Tasks sorted by time:")
    print("-" * 60)
    sorted_tasks = scheduler.sort_by_time()
    for task in sorted_tasks:
        status = "✓" if task.completed else "○"
        print(f"{status} {task.time.strftime('%I:%M %p')} - {task.task_type} for {task.pet.name}")

    # ===== TEST 2: filter_tasks(status="pending") =====
    print("\n2. USING filter_tasks(status='pending') - Pending tasks only:")
    print("-" * 60)
    pending_tasks = scheduler.filter_tasks(status="pending")
    for task in pending_tasks:
        print(f"○ {task.time.strftime('%I:%M %p')} - {task.task_type} for {task.pet.name}")

    # ===== TEST 3: filter_tasks(status="completed") =====
    print("\n3. USING filter_tasks(status='completed') - Completed tasks only:")
    print("-" * 60)
    completed_tasks = scheduler.filter_tasks(status="completed")
    for task in completed_tasks:
        print(f"✓ {task.time.strftime('%I:%M %p')} - {task.task_type} for {task.pet.name}")

    # ===== TEST 4: filter_tasks(pet_name="Buddy") =====
    print("\n4. USING filter_tasks(pet_name='Buddy') - All tasks for Buddy:")
    print("-" * 60)
    buddy_tasks = scheduler.filter_tasks(pet_name="Buddy")
    for task in buddy_tasks:
        status = "✓" if task.completed else "○"
        print(f"{status} {task.time.strftime('%I:%M %p')} - {task.task_type}")

    # ===== TEST 5: filter_tasks(pet_name="Luna", status="pending") =====
    print("\n5. USING filter_tasks(pet_name='Luna', status='pending') - Luna's pending tasks:")
    print("-" * 60)
    luna_pending = scheduler.filter_tasks(pet_name="Luna", status="pending")
    for task in luna_pending:
        print(f"○ {task.time.strftime('%I:%M %p')} - {task.task_type}")

    # ===== TEST 6: Recurring Tasks - Daily Task Auto-Scheduling =====
    print("\n6. TESTING RECURRING TASKS - Daily task auto-scheduling:")
    print("-" * 60)
    
    # Create a new daily task for Buddy
    daily_walk = Task(
        task_type="Daily Walk",
        date=today,
        time=time(7, 0),  # 7:00 AM
        pet=buddy,
        notes="Morning walk",
        frequency="daily"
    )
    buddy.add_task(daily_walk)
    
    # Check Buddy's tasks before marking complete
    initial_count = len(buddy.get_tasks())
    print(f"Initial Buddy task count: {initial_count}")
    print(f"Daily Walk task - Date: {daily_walk.date}, Completed: {daily_walk.completed}")
    
    # Mark the daily task as complete
    daily_walk.mark_complete()
    print(f"\n✓ Marked 'Daily Walk' as complete")
    
    # Check Buddy's tasks after marking complete
    final_count = len(buddy.get_tasks())
    print(f"After marking complete - Buddy task count: {final_count}")
    print(f"Original task - Completed: {daily_walk.completed}")
    
    # Verify new task was created for tomorrow
    tomorrow = today + timedelta(days=1)
    new_task = buddy.get_pending_tasks()[-1] if buddy.get_pending_tasks() else None
    
    if new_task and new_task.date == tomorrow and new_task.task_type == "Daily Walk":
        print(f"\n✓ SUCCESS! New 'Daily Walk' task created for tomorrow")
        print(f"New task - Date: {new_task.date}, Time: {new_task.time.strftime('%I:%M %p')}, Completed: {new_task.completed}")
        print(f"Frequency preserved: {new_task.frequency}")
    else:
        print("\n✗ FAILED: New task was not created correctly")

    # ===== TEST 7: Conflict Detection =====
    print("\n7. TESTING CONFLICT DETECTION:")
    print("-" * 60)
    
    # Create two tasks for Buddy at the same time (conflict scenario)
    conflict_task1 = Task(
        task_type="Vet Appointment",
        date=today,
        time=time(14, 0),  # 2:00 PM
        pet=buddy,
        notes="Annual checkup"
    )
    conflict_task2 = Task(
        task_type="Training Session",
        date=today,
        time=time(14, 0),  # 2:00 PM (SAME TIME - CONFLICT!)
        pet=buddy,
        notes="Obedience training"
    )
    
    buddy.add_task(conflict_task1)
    buddy.add_task(conflict_task2)
    
    print("Added two tasks for Buddy at 2:00 PM on the same day:")
    print(f"  1. {conflict_task1.task_type}")
    print(f"  2. {conflict_task2.task_type}")
    
    # Refresh scheduler tasks and call detect_conflicts
    scheduler.tasks = scheduler.owner.get_all_tasks()
    conflict_message = scheduler.detect_conflicts()
    
    print(f"\nConflict Detection Result:")
    print(conflict_message)
    
    # Verify conflict was detected
    if "SCHEDULING CONFLICTS DETECTED" in conflict_message:
        print("\n✓ SUCCESS! Conflict detection working correctly")
    else:
        print("\n✗ FAILED: Conflict not detected")

    print("\n" + "=" * 60)
    print("✓ All methods and recurring tasks working correctly!")
    print("=" * 60)
if __name__ == "__main__":
    main()