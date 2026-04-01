# PawPal+ Project Reflection

## 1. System Design

Core Actions (Step 1 in instructions):
1. Add a pet - The user can create a new pet profile with details like name, age, and breed.
2. Schedule and track tasks - The user can schedule and track daily tasks for a pet like feeding (with the type of food and amount), walks, medication reminders (with the dose).
3. View and manage appointments - The user can schedule appointments and view upcoming vet and grooming appointments, and get reminders when they are approaching. 


**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design has 4 classes: Owner, Pet, Task, and Scheduler.

Owner- stores the owner's name and a list of their pets. It can add and remove pets. 
Pet- Hold's the pet's name, breed, and age. It stores data.
Task- holds the task type like walk, feeding, medication, grooming, and vet appointment, and other like data, time, and notes like food amount or medication dose. 
Scheduler- holds a list of tasks and can add or remove tasks, get today's tasks and send reminders. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

After asking Copilot to review the skeleton, I made two changes to the Task class. 
1. I made pet a required field instead of optional because every task should always be linked to a pet. 
2. Reordered the fields in the Task dataclass so that required fields come before optional fields.


## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler considers time,status, pet, frequency, and conflicts.
I decided time was the most important constraint because 
a pet owner needs to know what to do and when, so sorting 
by time makes the schedule easy to follow.


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The detect_conflicts() method checks for exact time matches 
rather than overlapping durations. This means two tasks at 2:00 PM and 2:30 PM would NOT be flagged as a conflict even 
if they overlap. This tradeoff is reasonable because exact 
time matching is simpler to implement and understand, and 
for a basic pet care app it is good enough.

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used GitHub copilot through this project in several ways, to design brainstorming, code generation (like Agent mode), debugging when I had some issues, refactoring, testing, and some for algorithm design. The most helpful prompts were ones that included the file reference like the file pawpal_system.py and clearly described what I wanted the code to do.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One moment where I did not accept an AI suggestion as it was provided was when Copilot suggested using defaultdict to simplify the detect_conflicts() methods. I considered the suggestion and decided to keep the current version I had because it is easier to read and understand. I made sure the current version worked correctly by running the demo script and seeing the conflict detection output in the terminal. 

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested the task completion (the mark complete), task addition (Adding pet tasks increases the pet's task count by one), sorting correctness (chronological order), recurrence logic (marking a daily task complete automatically creates that task for the following day), conflict detection (correctly identifies two tasks schedule at the same time). 
These tests are important because they cover the main behaviors of this app, if any of these were to break the whole system stops working correctly.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am 4 out of 5 stars confident that my scheduler works correctly. All 5 tests passed and cover the main behavior. If I had more time I would test these edge cases: A task schedule at midnight, recurring task that crosses a month boundary like January 31 to February 1, filtering tasks if a pet has none.

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most happy with how I learned to use copilot in a very eficient way. The recurring tasks feature works exactly how I want it to work, when a daily task is marked complete, a new task is automatically created for the following day. I also really liked how the Streamlit UI came together and actually connects to real backend classes. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration I would improve the conflict detection, instead of only checking for exact time matches, I would check for overlapping durations. For example if a walk takes 30 minutes and starts at 2:00 PM, it should conflict with a task at 2:15 PM. And the UI, I would add the ability to delete pets and tasks, and add a calendar view so the owner can see their whole week at a glance instead of just one day at a time.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The most important thing I learned is that AI is a very powerful tool but you still must be the one to work as a "lead architect" Copilot can generate a lot of code really quickly but it is not capable of creating design decisions for me. I had to be able to understand the problem, be able to design the structure of it and being able to evaluare all of the suggestions Copilot made before accepting the suggestions. The best results come when I give Copilot very specific and detailed prompts instead of basic or vague ones. 
