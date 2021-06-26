# -*- coding: utf-8 -*-
from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np
import collections
import random
import math


import time
from numpy.random import randint
from collections import Counter
from random import shuffle
import random as rnd
import operator
from prettytable import PrettyTable

rooms_array = [[301, 28], [302, 28], [303, 28], [304, 28], [305, 28], [306, 28], [307, 28], [308, 28], [309, 28],
               [310, 28]]
Days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
Time = ["9-12", "12-3", "2-5"]
Time_Friday = ["9-12", "2-5"]
binary_number = 0
population_size = 9  # in every iteration kitnay cases we will be assuming
max_generations = 1  # kitni baar genetic algorithm ka function chalay gah
mutation_probability = 0.3
mutation_probability_2 = 0.8
mutation_probability_3 = 0.9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
max_generation = 0
studentCourse_1 = []
course_capacity = 0
teacher_capacity = 0
rooms_capacity = 0
courses = []
teachers = []
teachers_am = []
teachers_pm = []
rooms_available = []

courses_df = pd.read_csv("/content/drive/My Drive/OurData/courses.csv", header=None)
#print(courses_df) #courses id and names

studentName_df = pd.read_csv("/content/drive/My Drive//OurData/studentNames.csv", header=None)
#print(studentName_df) #student names

teacherName_df = pd.read_csv("/content/drive/My Drive/OurData/teachers.csv", header=None)
#print(teacherName_df) #teacher names

studentCourse_df = pd.read_csv("/content/drive/My Drive/OurData/studentCourse.csv", header=None)
#print(studentCourse_df)

class Courses:
    def __init__(self, id, name, binary):
        self.id = id
        self.name = name
        self.binary = binary

    def initialize(courses, courses_np):
        global binary_number
        skip = False
        for value in courses_np:
            binary_temp = format(binary_number, '08b')
            for course in courses:
                if course.id == value[0]:
                    skip = True
            if skip == False:
                courses.append(Courses(value[0], value[1], binary_temp))
                binary_number += 1
            skip = False

    def print(courses):
        for obj in courses:
            print(obj.id, obj.name, obj.binary, sep=' ')
        print("")

    def set_binary(self, binary):
        self.binary = binary

    def get_binary(self):
        return self.binary


class Names:
    def __init__(self, name):
        self.name = name

    def initialize(names, names_np):
        for value in names_np:
            names.append(Names(value[0]))

    def print(names):
        for obj in names:
            print(obj.name, sep=' ')
        print("")


class Teachers:
    def __init__(self, name, binary):
        self.name = name
        self.binary = binary

    def initialize(teachers, teachers_np):
        global binary_number
        for value in teachers_np:
            binary_temp = format(binary_number, '08b')
            teachers.append(Teachers(value[0], binary_temp))
            binary_number += 1
    def divide(teachers_am, teachers_pm, teachers):
        skip = False
        while len(teachers_am) != int(teacher_capacity/2):
            temp_teacher = random.choice(teachers)
            for teacher in teachers_am:
                if teacher == temp_teacher:
                    skip = True
            if skip == False:
                teachers_am.append(temp_teacher)
            skip = False

        for teacher in teachers:
            for teacher_am in teachers_am:
                if teacher == teacher_am:
                    skip = True
            if skip == False:
                teachers_pm.append(teacher)
            skip = False

    def print(teachers):
        for obj in teachers:
            print(obj.name, obj.binary, sep=' ')
        print("")


class Student_Course:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def initialize(studentCourse, studentCourse_np):
        for value in studentCourse_np:
            studentCourse.append(Student_Course(value[1], value[2]))

    def print(studentCourse):
        for obj in studentCourse:
            print(obj.name, obj.id, sep=' ')
        print("")


class Rooms:

    def __init__(self, number, seatingcapacity, binary):
        self.number = number
        self.seatingcapacity = seatingcapacity
        self.binary = binary
        self.noofstudents = 0

    def get_number(self):
        return self.number

    def set_noofstudents(self, number):
        self.noofstudents = number

    def get_seatingcapacity(self):
        return self.seatingcapacity

    def initialize(rooms_available, rooms_array):
        global binary_number
        for value in rooms_array:
            binary_temp = format(binary_number, '08b')
            rooms_available.append(Rooms(value[0], value[1], binary_temp))
            binary_number += 1

    def get_courseName(self):
        return self.name

    def get_courseId(self):
        return self.id

    def print(rooms_available):
        for obj in rooms_available:
            print(obj.number, obj.seatingcapacity, obj.binary, sep=' ')

    def get_binary(number):
        for obj in rooms_available:
            if (obj.number == number):
                return obj.binary


class Class:

    def __init__(self, course):
        self.room = None
        self.course = course
        self.teacher = None
        self.day = None
        self.time = None

    def set_room(self, room): self.room = room

    def set_course(self, course): self.course = course

    def set_instructor(self, teacher): self.teacher = teacher

    def set_day(self, day): self.day = day

    def set_time(self, time): self.time = time

    def get_room(self): return self.room

    def get_course(self): return self.course

    def get_id(self): return self.id

    def get_courseid(self): return self.course.id

    def get_instructor(self): return self.teacher

    def get_day(self): return self.day

    def get_time(self): return self.time

    def __str__(self):
        return (str(self.get_room()) + "," + str(self.get_course()) + "," + str(self.get_instructor()) + "," + str(
            self.get_day()) + "," + str(self.get_time()) + "--")

class Schedule:

    def __init__(self, course, teacher):
        self.course = course
        self.instructor = teacher
        self.room = []
        self.classes = []
        self.isFitnessChanged = True
        self.Number_of_Conflicts = 0
        self.binary_value = " "

    def get_Number_of_Conflicts(self):
        return self.Number_of_Conflicts

    def set_binary(self, value):
        self.binary_value = value

    def get_binary(self):
        return self.binary_value

    def Initialize(self):
        global rooms_available
        teacher_binary = None
        course_binanry = None
        room_binary = None
        for i in range(0, len(self.course)):
            numberofstudents = 0
            course_selected = Class(self.course[i])
            course_binary = self.course[i].binary
            day_selected = Days[rnd.randint(0, len(Days) - 1)]
            day_selected = Days[rnd.randint(0, len(Days) - 1)]
            if day_selected == "Friday" or day_selected == "Friday_2":
                time_selected = random.choice(Time_Friday)
            else:
                time_selected = random.choice(Time)
            for student in studentCourse_1:
                for j in range(1, len(student)):
                    if student[j] == course_selected.get_course().id:
                        numberofstudents += 1
            loop_value = math.ceil(numberofstudents / 28)
            remaning_students = numberofstudents
            for j in range(0, loop_value):
                newClass = Class(self.course[i])
                newClass.set_time(time_selected)
                room_temp = random.choice(rooms_array)

                room_binary = Rooms.get_binary(room_temp[0])

                room_selected = Rooms(room_temp[0], room_temp[1], room_binary)

                if numberofstudents < 28:
                    room_selected.set_noofstudents(numberofstudents)
                else:
                    room_selected.set_noofstudents(28)
                    numberofstudents -= 28

                newClass.set_room(room_selected)

                if (time_selected == "9-12"):
                    temp_teacher = random.choice(teachers_am)

                    teacher_binary = temp_teacher.binary

                else:
                    temp_teacher = random.choice(teachers_pm)

                    teacher_binary = temp_teacher.binary

                newClass.set_instructor(temp_teacher)
                newClass.set_day(day_selected)
           
                self.classes.append(newClass)

                self.binary_value = course_binary + teacher_binary + room_binary

        return self

    def get_classes(self):
        self.isFitnessChanged = True
        return self.classes

    def calculate_fitness_2(self):
        course_conflict = False
        
        classes = self.get_classes()
        self.Number_of_Conflicts = 0
        for i in range(0, len(classes)):
            for j in range(0, len(classes)):
                if j > i:
                    if classes[i].get_day() == classes[j].get_day():
                        if classes[i].get_time() == classes[j].get_time():
                            if classes[i].get_room() == classes[j].get_room():
                                
                                self.Number_of_Conflicts += 1
                                room_temp = random.choice(rooms_array)
                                
                                print("2 Courses at same time in same room")
                                print(classes[i].get_course().name, " & ", classes[j].get_course().name)

                    if classes[i].get_course() == classes[j].get_course():
                        if classes[i].get_day() != classes[j].get_day() or classes[i].get_time() != classes[j].get_time():
                            self.Number_of_Conflicts += 1
                            print("Same courses at different time/day")
                            print(classes[i].get_course().name, " &", classes[j].get_course().name)

                    # To ensure the same teacher isn't invigilating two different exams at the same time
                    if classes[i].get_instructor() == classes[j].get_instructor():
                        if classes[i].get_day() == classes[j].get_day():
                            if classes[i].get_time() == classes[j].get_time():
                                print("Teacher invigilating 2 exams at same time")
                                print(classes[i].get_instructor().name, classes[i].get_day(), classes[i].get_time())
                               
                                self.Number_of_Conflicts += 1

                    # To ensure the same teacher isn't invigilating an exam from 12-3 & 2-5
                    if classes[i].get_instructor() == classes[j].get_instructor():
                        if classes[i].get_day() == classes[j].get_day():
                            if classes[i].get_time() == "12-3" and classes[j].get_time() == "2-5" or classes[i].get_time() == "2-5" and classes[j].get_time() == "12-3":
                                print("Teacher invigilating 2 exams at conflicting times")
                                print(classes[i].get_instructor().name, classes[i].get_day())
                                
                                self.Number_of_Conflicts += 1


        # For MG Courses
        for i in range(0, len(classes)):
            if classes[i].get_course().id[:2] == "MG":
                
                if classes[i].get_time() == "12-3" or classes[i].get_time() == "2-5":
                    print("MG exam not in morning")
                    self.Number_of_Conflicts += 1

        # Ensure gap from 1-2 on Friday
        for i in range(0, len(classes)):
            if classes[i].get_day() == "Friday" and classes[i].get_time() == "12-3" or classes[
                i].get_day() == "Friday_2" and classes[i].get_time() == "12-3" or classes[i].get_day() == "Friday_3" and \
                    classes[i].get_time() == "12-3":
                self.Number_of_Conflicts += 1
                print("Friday exam at from 12-3")

        # Check if an AM teacher invigilating an PM exam
        for i in range(0, len(classes)):
            if classes[i].get_time() == "12-3" or classes[i].get_time() == "2-5":
                for j in range(0, len(teachers_am)):
                    if teachers_am[j] == classes[i].get_instructor():
                        print("AM teacher invigilating PM Exam")
                        
                        self.Number_of_Conflicts += 1

        # Check if an PM teacher invigilating an AM exam
        for i in range(0, len(classes)):
            if classes[i].get_time() == "9-12":
                for j in range(0, len(teachers_pm)):
                    if teachers_pm[j] == classes[i].get_instructor():
                        
                        print("PM teacher invigilating AM Exam")
                        
                        self.Number_of_Conflicts += 1
    

        for student in studentCourse_1:
            for i in range(0, len(classes)):
                for j in range(1, len(student)):
                    if student[j] == classes[i].get_course().id: 
                        for k in range(j + 1, len(student)):
                            for l in range(i + 1, len(classes)):
                                if student[k] == classes[l].get_course().id:
                                    if classes[i].get_day() == classes[l].get_day():
                                        if classes[i].get_time() == classes[l].get_time() or classes[
                                            i].get_time() == "9-12" and classes[l].get_time() == "12-3" or classes[
                                            i].get_time() == "12-3" and classes[l].get_time() == "2-5" or classes[
                                            i].get_time() == "12-3" and classes[l].get_time() == "9-12" or classes[
                                            i].get_time() == "2-5" and classes[l].get_time() == "12-3":
                                            print("Student has exams at same time")
                                            self.Number_of_Conflicts += 1
        return 1 / ((1.0 * self.Number_of_Conflicts + 1))

    def calculate_fitness(self):
        course_conflict = False
        classes = self.get_classes()
        self.Number_of_Conflicts = 0
        for i in range(0, len(classes)):
            for j in range(0, len(classes)):
                if j > i:
                    if classes[i].get_day() == classes[j].get_day():
                        if classes[i].get_time() == classes[j].get_time():
                            if classes[i].get_room() == classes[j].get_room():
                                
                                self.Number_of_Conflicts += 1

                    if classes[i].get_course() == classes[j].get_course():
                        if classes[i].get_day() != classes[j].get_day() or classes[i].get_time() != classes[
                            j].get_time():
                            self.Number_of_Conflicts += 1

                    # To ensure the same teacher isn't invigilating two different exams at the same time
                    if classes[i].get_instructor() == classes[j].get_instructor():
                        if classes[i].get_day() == classes[j].get_day():
                            if classes[i].get_time() == classes[j].get_time():
                                # print("Conflict Encountered")
                                self.Number_of_Conflicts += 1

                    #To ensure the same teacher isn't invigilating an exam from 12-3 & 2-5
                    if classes[i].get_instructor() == classes[j].get_instructor():
                        if classes[i].get_day() == classes[j].get_day():
                            if classes[i].get_time() == "12-3" and classes[j].get_time() == "2-5" or classes[i].get_time() == "2-5" and classes[j].get_time() == "12-3":
                                # print("Conflict Encountered")
                                self.Number_of_Conflicts += 1

                    # To make sure MG exams happen before CS

        # For MG Courses
        for i in range(0, len(classes)):
            if classes[i].get_course().id[:2] == "MG":
                if classes[i].get_time() == "12-3" or classes[i].get_time() == "2-5":
                    self.Number_of_Conflicts += 1

        # Ensure gap from 1-2 on Friday
        for i in range(0, len(classes)):
            if classes[i].get_day() == "Friday" and classes[i].get_time() == "12-3" or classes[
                i].get_day() == "Friday_2" and classes[i].get_time() == "12-3" or classes[i].get_day() == "Friday_3" and \
                    classes[i].get_time() == "12-3":
                self.Number_of_Conflicts += 1

        # Check if an AM teacher invigilating an PM exam
        for i in range(0, len(classes)):
            if classes[i].get_time() == "12-3" or classes[i].get_time() == "2-5":
                for j in range(0, len(teachers_am)):
                    if teachers_am[j] == classes[i].get_instructor():
                        
                        self.Number_of_Conflicts += 1

        # Check if an PM teacher invigilating an AM exam
        for i in range(0, len(classes)):
            if classes[i].get_time() == "9-12":
                for j in range(0, len(teachers_pm)):
                    if teachers_pm[j] == classes[i].get_instructor():
                        
                        self.Number_of_Conflicts += 1

        for student in studentCourse_1:
            for i in range(0, len(classes)):
                for j in range(1, len(student)):
                    if student[j] == classes[i].get_course().id:
                        for k in range(j + 1, len(student)):
                            for l in range(i + 1, len(classes)):
                                if student[k] == classes[l].get_course().id:
                                    if classes[i].get_day() == classes[l].get_day():
                                        if classes[i].get_time() == classes[l].get_time() or classes[
                                            i].get_time() == "9-12" and classes[l].get_time() == "12-3" or classes[
                                            i].get_time() == "12-3" and classes[l].get_time() == "2-5" or classes[
                                            i].get_time() == "12-3" and classes[l].get_time() == "9-12" or classes[
                                            i].get_time() == "2-5" and classes[l].get_time() == "12-3":
                                            self.Number_of_Conflicts += 1
        return 1 / ((1.0 * self.Number_of_Conflicts + 1))

    def get_fitness(self):
        if (self.isFitnessChanged == True):
            self.fitness = self.calculate_fitness()
            self.isFitnessChanged = False
        return self.fitness

    def __str__(self):
        returnValue = ""
        for i in range(0, len(self.classes)):
            returnValue += str(self.classes[i].get_room().number) + " " + str(
                self.classes[i].get_room().noofstudents) + " " + str(self.classes[i].get_course().name) + " " + str(
                self.classes[i].get_instructor().name) + ","
       
        return returnValue


class GeneticAlgorithm:

    def __init__(self, size, course, instructor):
        self.size = size
        self.course = course
        self.instructor = instructor

    def start(self, population):
        return self.mutate_pop(self.crossoverpopulation(population))

    def crossoverpopulation(self, pop):
        cross_pop = Population(self.size, self.course, self.instructor)

        for i in range(NUMB_OF_ELITE_SCHEDULES):
            cross_pop.get_schedules().append(pop.get_schedules()[i])

        i = NUMB_OF_ELITE_SCHEDULES

        while i < self.size:
            schedule1 = self.select_population(pop).get_schedules()[0]
            schedule2 = self.select_population(pop).get_schedules()[0]
            
            s1, s2 = self._crossover_schedule(schedule1, schedule2)
            cross_pop.get_schedules().append(s1)
            cross_pop.get_schedules().append(s2)
            i += 1
        return cross_pop

    def mutate_pop(self, population):
        for i in range(NUMB_OF_ELITE_SCHEDULES, population_size - 1):
            if rnd.randint(0, 2) == 0:
                self.mutate_1(population.get_schedules()[i], population.get_schedules()[i + 1])
            else:
                self.mutate_schedule(population.get_schedules()[i])
            self.mutate_schedule(population.get_schedules()[i])
        return population

    def _crossover_schedule(self, schedule1, schedule2):
        
        c1 = schedule2.course
        c2 = schedule1.course
        schedule1.course = c1
        schedule2.course = c2

        return schedule1, schedule2

    def mutate_1(self, mutateSchedule1, mutateSchedule2):
        mutate_copy = Schedule(self.course, self.instructor).Initialize()
        for i in range(0, len(mutateSchedule1.get_classes())):
            number = rnd.random()
            k = 0
            
            if (mutation_probability > number):
                
                for j in range(len(mutateSchedule1.get_classes())):
                    if mutateSchedule2.get_classes()[i].get_course().binary != mutateSchedule1.get_classes()[j].get_course().binary:
                        
                        mutate_copy.get_classes()[k] = mutateSchedule1.get_classes()[j]
                        k += 1
                    
                for j in range(len(mutateSchedule2.get_classes())):
                    if mutateSchedule2.get_classes()[i].get_course().binary == mutateSchedule2.get_classes()[
                        j].get_course().binary:
                        
                        mutate_copy.get_classes()[k] = mutateSchedule2.get_classes()[j]
                        k += 1
                    
                mutateSchedule1 = mutate_copy

        return mutateSchedule1

    def mutate_schedule(self, mutateSchedule):

        schedule = Schedule(self.course, self.instructor).Initialize()
        mutate_copy = Schedule(self.course, self.instructor).Initialize()
        for i in range(0, len(mutateSchedule.get_classes())):
            number = rnd.random()
            number_2 = rnd.random()
            number_3 = rnd.random()
            k = 0
            # print("NUMBER =" ,number)
            if (mutation_probability > number):
                # print("IN MUTATION ", mutateSchedule.get_classes()[i].get_course().name)
                # mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
                # print("I", i, schedule.get_classes()[i].get_course().name)
                for j in range(len(mutateSchedule.get_classes())):
                    if schedule.get_classes()[i].get_course().binary != mutateSchedule.get_classes()[j].get_course().binary:
                        # print("COPYING from Mutate= ",(mutateSchedule.get_classes()[j].get_course().name, mutateSchedule.get_classes()[j].get_day(), mutateSchedule.get_classes()[j].get_time()))
                        mutate_copy.get_classes()[k] = mutateSchedule.get_classes()[j]
                        if mutation_probability_2 > number_2:
                            mutate_copy.get_classes()[k].set_instructor(schedule.get_classes()[j].get_instructor())
                        if mutation_probability_3 > number_3:
                            mutate_copy.get_classes()[k].set_room(schedule.get_classes()[j].get_room())
                        k += 1
                    # print(k)
                for j in range(len(schedule.get_classes())):
                    if schedule.get_classes()[i].get_course().binary == schedule.get_classes()[j].get_course().binary:
                        # print("COPYING from Schedule= ",(schedule.get_classes()[j].get_course().name, schedule.get_classes()[j].get_day(), schedule.get_classes()[j].get_time()))
                        mutate_copy.get_classes()[k] = schedule.get_classes()[j]
                        k += 1
                    # print(k)
                mutateSchedule = mutate_copy

        return mutateSchedule

    def select_population(self, pop):
        
        tournament_pop = Population(self.size, self.course, self.instructor)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0, self.size)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop


def generation_print(population):
    table1 = PrettyTable(['schedule #', 'fitness', '# of conflict', 'Classes'])
    schedules = population.get_schedules()
    print("len of schedules: ", len(schedules))
    for i in range(0, len(schedules)):
        table1.add_row(
            [str(i), round(schedules[i].get_fitness(), 3), schedules[i].get_Number_of_Conflicts(), schedules[i]])
    print(table1)


def print_schedule_table(schedule):
    classes = schedule.get_classes()

    table = PrettyTable(['Day', 'Time', 'Course', 'Instructor', 'Room', 'NoofStudents'])
    for i in range(0, len(classes)):
        table.add_row(
            [classes[i].get_day(), classes[i].get_time(), classes[i].get_course().name,
             classes[i].get_instructor().name,
             classes[i].get_room().number, classes[i].get_room().noofstudents])
    print(table.get_string(sortby=('Day')))


class Population:

    def __init__(self, size, course, instructor):
        self.size = size
        self.course = course
        self.instructor = instructor
        self.schedules = []

        for i in range(0, size):
            self.schedules.append(Schedule(course, instructor).Initialize())

    def get_schedules(self):
        return self.schedules


if __name__ == "__main__":

    courses_np = np.array(courses_df.values.tolist())
    Courses.initialize(courses, courses_np)
    Courses.print(courses)
    course_capacity = len(courses)
    print(course_capacity)

    names_np = np.array(studentName_df.values.tolist())
    names = []
    Names.initialize(names, names_np)
    Names.print(names)

    teachers_np = np.array(teacherName_df.values.tolist())

    Teachers.initialize(teachers, teachers_np)
    Teachers.print(teachers)
    teacher_capacity = len(teachers)
    Teachers.divide(teachers_am, teachers_pm, teachers)

    print("AM")
    Teachers.print(teachers_am)
    print("PM")
    Teachers.print(teachers_pm)

    for teacher_am in teachers_am:
        for teacher_pm in teachers_pm:
            if teachers_am == teachers_pm:
                print("DUPLICATION")

    studentCourse_np = np.array(studentCourse_df.values.tolist())
    studentCourse = []
    Student_Course.initialize(studentCourse, studentCourse_np)
    # Student_Course.print(studentCourse)

    visited = []
    studentCourse_1 = []
    found = False
    course_found = False
    for i in range(len(studentCourse_np)):
        found = False
        count = 0
        for obj in visited:
            
            if obj == studentCourse_np[i][1]:
                found = True
        if found == False:
            courses_ = []
            courses_.append(studentCourse_np[i][1])
            for j in range(i, len(studentCourse_np)):
                course_found = False
                if found == False and studentCourse_np[j][1] == studentCourse_np[i][1]:
                    for course in courses_:
                        if course == studentCourse_np[j][2]:
                            
                            course_found = True
                    if course_found == False:
                        count += 1
                        courses_.append(studentCourse_np[j][2])
            if count >= 3:
               
                visited.append(studentCourse_np[i][1])
                studentCourse_1.append(courses_)
            if count < 3:
                print("COUNT LESS THAN 3")
                print(studentCourse_np[i][1])
        

    for i in range(len(studentCourse_1)):
        print(studentCourse_1[i])

    print("Rooms Available: \n")
    Rooms.initialize(rooms_available, rooms_array)
    Rooms.print(rooms_available)
    rooms_capacity = len(rooms_available)
    print("\n")

    population = Population(population_size, courses, teachers)
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    generation_print(population)
    print_schedule_table(population.get_schedules()[0])
    ga = GeneticAlgorithm(population_size, courses, teachers)
    generations = 0
    while population.get_schedules()[0].get_fitness() != 1 or generations < 45:
        print("GENERATIONS= ", generations)
        population = ga.start(population)
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        generation_print(population)
        print_schedule_table(population.get_schedules()[0])
        population.get_schedules()[0].calculate_fitness_2()
        generations += 1
        if generations == 45 or population.get_schedules()[0].get_fitness() == 1:
            break
    print_schedule_table(population.get_schedules()[0])
