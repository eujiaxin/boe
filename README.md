
# PVC IT Challenge Submission

Name of Group: BoE  
Name of Project: BoE  
| Group Member          	| Github Handle                               	| Role               	|
|-----------------------	|---------------------------------------------	|--------------------	|
| Fabian Lim (3)        	| [旭淮](https://github.com/Weiss01)          	| Team Lead, Backend 	|
| Eu Jia Xin (30881676) 	| [heheheejin](https://github.com/heheheejin) 	| Frontend           	|

## Introduction to BoEasy
[video]

## Core Features of Application
#### Features offered by Innovation
To handle various types of course offerings across different faculties, our system breaks each course down into different levels of abstraction. These different layers are represented as Django model objects, and are processed by linking them together in a graph system. A complex course graph is formed and receives students' data input to be traversed.

Relevant staffs who are responsible of the course data should have a fair understanding of [how this system works](#detailed-explanation-of-application--examples) in order to properly create or update a course.

#### List of possible enabling technologies
Currently, the system uses SQLite to store courses and student data. In the future, database migration to [PostgreSQL](https://www.postgresql.org/) can be done for better scalability.

#### List of library dependencies
* [Django](https://www.djangoproject.com/) 
* [Bootstrap](https://getbootstrap.com/)

#### Others
* [Django authentication system](https://docs.djangoproject.com/en/4.0/topics/security/) protects sensitive data such as user credentials and guards against SQL injections.
* Once hosted on a server, the application system will be online 24/7 and is able to handle concurrent users by allowing multiple logins from different parties at the same time.
* Users are allowed to upload more than 1 spreadsheet in a single request. After uploading the files, the final output shown includes all students in the selected uploaded files.

## Detailed Explanation of Application & Examples
(include simple table of CSV and the output then explain how it happens)
## Selection Criteria
#### Cost of Implementation
Hosting the applicaton system on a server ([AWS EC2](https://aws.amazon.com/ec2/)) costs 337 USD per year.
#### Ease of Implementation
Current application system can be readily hosted and be tested by the Education Management Offices (EMO) staffs.

#### Ease of serviceability and maintenance
Courses have to be updated by BoE administrators or other relevant staff following the format of our solution. 

To sustain the implementation of the proposed solution, the database containing course details (core units and elective units required) should be updated by relevant staff whenever there is a change to courses.  
  
In the future, a user-friendly interface would be provided for the Education Management Offices (EMO) staff to update existing courses, or create new courses. Once the courses have been processed by the application system and saved into the database,  the system will be able to process CSV uploads of students enrolled in the courses. 

#### Documentation
* UML Diagram and detailed explanation of how the processing algorithm works are provided for future technical members.
#### Risk
* ???
