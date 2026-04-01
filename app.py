import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date, time, timedelta

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+")
st.subheader("Pet Care Planning Assistant")

# ============================================================================
# Initialize session_state with Owner object
# ============================================================================
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Alex")

owner = st.session_state.owner

# ============================================================================
# Sidebar: Owner Management
# ============================================================================
with st.sidebar:
    st.header("Owner Profile")
    st.write(f"**Owner:** {owner.name}")
    st.write(f"**Pets:** {len(owner.get_pets())}")
    
    st.divider()
    
    # Change owner name
    new_owner_name = st.text_input("Update owner name", value=owner.name)
    if st.button("Update Name"):
        owner.name = new_owner_name
        st.success("✅ Owner name updated!")

# ============================================================================
# Main Content: Add a Pet
# ============================================================================
st.header("Add a Pet")
col1, col2, col3, col4 = st.columns(4)

with col1:
    pet_name = st.text_input("Pet name", value="Buddy")
with col2:
    pet_species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Hamster", "Other"])
with col3:
    pet_breed = st.text_input("Breed", value="Golden Retriever")
with col4:
    pet_age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)

if st.button("Add Pet", key="add_pet_btn"):
    # Check if pet already exists
    existing_names = [pet.name for pet in owner.get_pets()]
    if pet_name in existing_names:
        st.warning(f"⚠️ A pet named '{pet_name}' already exists!")
    else:
        new_pet = Pet(name=pet_name, breed=pet_breed, species=pet_species, age=pet_age)
        owner.add_pet(new_pet)
        st.success(f"✅ Successfully added {pet_name} the {pet_species}!")

st.divider()

# ============================================================================
# List Current Pets
# ============================================================================
if owner.get_pets():
    st.subheader("Your Pets")
    for pet in owner.get_pets():
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        with col1:
            st.write(f"**{pet.name}**")
        with col2:
            st.write(f"Species: {pet.species}")
        with col3:
            st.write(f"Breed: {pet.breed} | Age: {pet.age}yrs")
        with col4:
            st.write(f"Tasks: {len(pet.tasks)}")
else:
    st.info("No pets yet. Add one above!")

st.divider()

# ============================================================================
# Add a Task
# ============================================================================
st.header("Add a Task")

if owner.get_pets():
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        selected_pet = st.selectbox("Select Pet", [pet.name for pet in owner.get_pets()])
    
    with col2:
        task_type = st.selectbox("Task Type", ["Walk", "Feeding", "Medication", "Grooming", "Play Time", "Vet Appointment", "Other"])
    
    with col3:
        task_time = st.time_input("Time", value=time(14, 0))
    
    with col4:
        task_notes = st.text_input("Notes (optional)", value="")
    
    if st.button("Add Task", key="add_task_btn"):
        # Find the selected pet
        selected_pet_obj = next((p for p in owner.get_pets() if p.name == selected_pet), None)
        
        if selected_pet_obj:
            new_task = Task(
                task_type=task_type,
                date=date.today(),
                time=task_time,
                pet=selected_pet_obj,
                notes=task_notes
            )
            selected_pet_obj.add_task(new_task)
            st.success(f"✅ Added '{task_type}' task for {selected_pet}!")
else:
    st.warning("⚠️ Please add a pet first before creating tasks.")

st.divider()

# ============================================================================
# Today's Schedule
# ============================================================================
st.header("📅 Today's Schedule")

scheduler = Scheduler(owner)

# Check for scheduling conflicts
conflict_message = scheduler.detect_conflicts()
if "SCHEDULING CONFLICTS DETECTED" in conflict_message:
    st.warning(f"⚠️ {conflict_message}")

todays_tasks = scheduler.get_todays_tasks()

# Use sort_by_time() to ensure chronological order
todays_tasks = scheduler.sort_by_time() if todays_tasks else []
todays_tasks = [t for t in todays_tasks if t.date == date.today()]

if todays_tasks:
    st.success(f"✓ {len(todays_tasks)} tasks scheduled for today")
    st.subheader(f"Tasks for {date.today()}")
    
    for idx, task in enumerate(todays_tasks, 1):
        col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 3, 1])
        
        with col1:
            # Checkbox for completion
            is_completed = st.checkbox("Done", value=task.completed, key=f"task_complete_{idx}")
            if is_completed != task.completed:
                if is_completed:
                    task.mark_complete()
                    st.success(f"✓ Marked '{task.task_type}' as complete")
                else:
                    task.completed = False
        
        with col2:
            st.write(f"**{task.time.strftime('%I:%M %p')}**")
        
        with col3:
            st.write(f"**{task.task_type}**")
        
        with col4:
            st.write(f"{task.pet.name} ({task.pet.species})")
            if task.notes:
                st.caption(f"📝 {task.notes}")
        
        with col5:
            status_emoji = "✓" if task.completed else "○"
            st.write(status_emoji)
    
    # Summary statistics
    st.divider()
    completed_count = len([t for t in todays_tasks if t.completed])
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Tasks", len(todays_tasks))
    with col2:
        st.metric("Completed", completed_count)
    with col3:
        st.metric("Pending", len(todays_tasks) - completed_count)
else:
    st.info("📋 No tasks scheduled for today. Add some tasks above!")
