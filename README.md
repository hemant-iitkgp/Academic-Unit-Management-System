# Academic Unit Management System
This is a Python-based software application designed for managing profiles in an academic unit. The system supports user registration, authentication, and profile management for different user types, such as teachers and students (UG and PG). It features an interactive GUI built with Tkinter and ensures secure and persistent data handling through CSV storage.

# Features
1. User Registration
Users can register with a unique ID and a secure password.
Password validation ensures security, enforcing length, uppercase, digit, and special character rules.
2. Authentication
Login functionality with account deactivation after three failed attempts to enhance security.
Differentiated access based on user types: Teacher, UG Student, PG Student.
3. Profile Management
Create and update user profiles with attributes specific to each user type.
Teacher: Post, Warden.
Student (UG/PG): Year of admission, CGPA, Hall, Research Area (for PG students).
4. Deregistration
Users can deregister their accounts, logically deactivating their profiles.
5. Graphical User Interface
Built using Tkinter for a seamless and interactive user experience.
Separate workflows and input forms for different user types.
6. Data Persistence
Uses CSV files to store and retrieve user data, ensuring persistence and portability.
# Class Hierarchy
The project employs an object-oriented design with the following hierarchy:

Person (Base class)
Teacher
Student
UG Student
PG Student
This structure showcases the use of OOP principles like inheritance and encapsulation.

# Getting Started
Prerequisites
Python 3.x
Required libraries: tkinter, csv, re

# System Demo
Refer to the included Documentation PDF for a detailed demo of the system, along with screenshots and an explanation of its functionality.

# Technologies Used
Python: Application logic and OOP implementation.
Tkinter: GUI development.
CSV: Data storage and retrieval.
# Documentation
The repository includes a PDF document titled Lab-4 Software Application Using Python, which contains:

A detailed overview of the system.
Use case explanations.
Screenshots showcasing different functionalities.
# Future Improvements
Transition to a database for enhanced scalability and performance.
Implementation of advanced security features like encrypted passwords.
Addition of more user roles and features.
