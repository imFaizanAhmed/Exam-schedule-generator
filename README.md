# time-table-generator
In this project, time table was generated using a classical Artificial interlligence algorithm called Generic Algorithm. 
The success of solution is estimated on fulfillment of given constraints and criteria. Results of testing the algorithm show that all hard constraints are satisfied, while additional criteria are optimized to a certain extent.

## Constraints
There are set of constraints that I fulfilled.

### Hard Constraints
• An exam will be scheduled for each course.
• A student is enrolled in at least 3 courses. A student cannot give more than 1 exam at a time.
• Exam will not be held on weekends.
• Each exam must be held between 9 am and 5 pm
• Each exam must be invigilated by a teacher. A teacher cannot invigilate two exams at the same
time.
• A teacher cannot invigilate two exams in a row.
The above-mentioned constraints must be satisfied.

### Soft Constraints
• All students and teachers shall be given a break on Friday from 1-2.
• A student shall not give more than 1 exam consecutively.
• If a student is enrolled in a MG course and a CS course, it is preferred that their MG course exam be held before their CS course exam. 
• Two hours of break in the week such that at least half the faculty is free in one slot and the rest of the faculty is free in the other slot so the faculty meetings shall be held in parts as they are now.

## Input & Output
Input data for each exam are teachers’ names, students’, exam duration, courses (course codes), and list of allowed classrooms.
Output data are classroom and starting time for each exam along with course code and invigilating teacher. Time is determined by day (Monday to Friday) and start hour of the exam.
• Output is a chromosome which satisfies all hard constraints and soft constraints. 
• I displaied a list of all hard and soft constraints which are fulfilled in the output along with the fitness values at each iteration.

## Execution
To run this code your have to upload the dataset to google drive. Then run it on the google colab
