
# PVC IT Challenge Submission

Name of Group: BoEasy Group  
Name of Project: BoE  
| Group Member          	| Github Handle                               	|
|-----------------------	|---------------------------------------------	|
| Fabian Lim (3)        	| [旭淮](https://github.com/Weiss01)          	|
| Eu Jia Xin (30881676) 	| [heheheejin](https://github.com/heheheejin) 	|

## Introduction to BoEasy
[video]

## Core Features of Application
#### Features offered by Innovation
Our solution focuses on being as simple and minimalistic as possible while also providing all the required features and information to automate the process of validating a student's progress in their courses. To handle various types of course offerings across different faculties, our system breaks each course down into different levels of abstraction. These different layers are represented as Django model objects, and are processed by linking them together in a graph system. A complex course graph is formed and receives students' data input to be traversed.

Every student's past enrolments and grades are stored in our database to ensure consistency of the input data and accuracy of our output. This means that even if the new input data is missing old enrolment data, our solution will still work perfectly fine.

Relevant staffs who are responsible of the course data should have a fair understanding of [how course requirements are abstracted](#detailed-explanation-of-application--examples) in order to properly create or update a course.

#### List of possible enabling technologies
Currently, the system uses SQLite to store courses and student data. In the future, database migration to [PostgreSQL](https://www.postgresql.org/) can be done for better scalability.

#### List of library dependencies
* asgiref==3.4.1
* Django==4.0
* django-extensions==3.1.5
* djangorestframework==3.13.1
* numpy==1.21.5
* pandas==1.3.5
* python-dateutil==2.8.2
* pytz==2021.3
* six==1.16.0
* sqlparse==0.4.2
* tzdata==2021.5

#### Others
* [Django authentication system](https://docs.djangoproject.com/en/4.0/topics/security/) protects sensitive data such as user credentials and guards against SQL injections.
* Once hosted on a server, the application system will be online 24/7 and is able to handle concurrent users by allowing multiple logins from different parties at the same time.
* Users are allowed to upload more than 1 spreadsheet in a single request. After uploading the files, the final output shown includes all students in the selected uploaded files.

## Detailed Explanation of Application & Examples
(include simple table of CSV and the output then explain how it happens)
## Selection Criteria
#### Cost of Implementation
Hosting the applicaton system on an m6g.medium [AWS EC2](https://aws.amazon.com/ec2/) instance should be sufficient for the scale of this application and would cost ~337 USD per year.

#### Ease of Implementation
Current application system can be readily hosted on any computer with the listed dependencies and be tested by the Education Management Offices (EMO) staffs. Hosting our application on an [AWS EC2](https://aws.amazon.com/ec2/) instance is also as easy and as straightforward as renting and running a few line of commands.

#### Ease of serviceability and maintenance
Courses have to be added/updated by BoE administrators or other relevant staff following the format of our solution. Maintenece is streamline as the source code has been modularized as much as possible according to Django's best practices.

To sustain the implementation of the proposed solution, the database containing course details (core units and elective units required) can be updated by relevant staff whenever there is a change to courses.  
  
In the future, a user-friendly drag-and-drop interface would be provided for the Education Management Offices (EMO) staff to update existing courses, or create new courses. Once the courses have been processed by the application system and saved into the database,  the system will be able to process CSV uploads of students enrolled in the courses. 

#### Documentation
* UML Diagram and detailed explanation of how the processing algorithm works are provided for future technical members.

#### Future Implementations

We carefully planned our solution for useful and important features and laid the groundwork that will ease extending the code in the future. Features that can be readily implemented and was included in our solution's initial plan includes

* React Frontend for more streamlined development process
* Graph reports for a holistic overview of the validation output
* Automated emails to inform the students about the requirements that they are missing in order to graduate
* Asynchronous processing of intensive operations to accomodate for more concurrent users
* Intuitive and interactive drag-and-drop interface for creating new course requirements
