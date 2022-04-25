

# PVC IT Challenge Submission


Name of Group: BoEasy Group  
Name of Project: BoEasy  
Placement: Second runner-up

| Group Member          	| Github Handle                               	| Role |
|-----------------------	|---------------------------------------------	| -------------------------------------------
| Fabian Lim (30883113)        	| [旭淮](https://github.com/Weiss01)             | Tech Lead 1 |
| Eu Jia Xin (30881676) 	| [heheheejin](https://github.com/heheheejin) 	| Tech Lead 2 |

## Introduction to BoEasy
[Link to Video](https://drive.google.com/drive/u/0/folders/1CiYPtzT5enEIZUYvyzJPBSKdMWm_6CvN)  
Note: Video is only accessible to Monash University email accounts.

## Quickstart Guide
[Instructions to setup the application](https://github.com/heheheejin/boe/blob/master/HowToRun.md)  
Note: The quickstart guide assumes that `python3` is already installed in the user's machine

## Core Features of Application
#### Features offered by Innovation
Our solution focuses on being as simple and minimalistic as possible while also providing all the required features and information to automate the process of validating a student's progress in their courses. To handle various types of course offerings across different faculties, our system breaks each course down into different levels of abstraction. These different layers are represented as Django model objects, and are processed by linking them together in a graph system. A complex course graph is formed and receives students' data input to be traversed.

Every student's past enrolments and grades are stored in our database to ensure consistency of the input data and accuracy of our output. This means that even if the new input data is missing old enrolment data, our solution will still work perfectly fine.

Relevant staffs who are responsible of the course data should have a fair understanding of [how course requirements are abstracted](https://github.com/heheheejin/boe/blob/master/README.md#understanding-the-graph-structure) in order to properly create or update a course.

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


## User guide to application system 
1. Homepage  
![Homepage](https://i.ibb.co/1zjd45X/image.png)
	* Enter name of staff using the application
	* Upload a single or multiple CSV files in one request
	* Click on upload to process the CSV files

2. Processing page  
![ProcessPage](https://i.ibb.co/Vtg9V52/image.png)
	* Processed CSV files will be marked ✅
	* Users are allowed to select multiple CSV files, including previously processed CSV files.
	* After clicking on Process button, the page will be redirected to a single combined output based on the selected CSV files.

3. Student Info page  
![StudentPage](https://i.ibb.co/rwJhPwJ/image.png)
	* Students and the relevant course taken will be displayed.
	* Upon clicking `Validate!` button, users will be redirected to the final processed page.

4. Final processed page  
![FinalPage](https://i.ibb.co/H4K1Y9z/image.png)
	* **Completed Course Modules** - course completed by student (major/minor/specialisation)
	* **Pending Course Module** - incomplete course module needed to be taken in order to graduate
	*  **Missing Cores** - missing core units
	* **Completion status** - shows whether a student is eligible to graduate
		* `CORE INCOMPLETE` - missing core units required for course completion
		* `FREE ELECTIVE INCOMPLETE `- missing credit points from elective units required for course completion
		* ✅ - completed all core units and elective units with sufficient credit points, hence eligible for course completion.
		* 🟥 - student is enrolled in a course not found in our database.
        * Example 1: *Alexander Morgan* still needs to take FIT3045 to complete his course.
        * Example 2: *Pippa Smith* and *Adrian Mathis* both completed all core units and elective units required, therefore are eligible to graduate.
 
 ## Detailed Explanation of Application
 ### How does BoEasy handle course requirements?
 Referring to the Monash Handbook, different courses have vastly different requirements and structure. The requirements provided in the handbook are not systematic, which means that scraping directly from the handbook may cause the system application to output inaccurate results.
 
 BoEasy aims to pre-process course requirements into a systematic graph structure, where any student enrolment data can be processed using the graph.
 
### Understanding the graph structure

Example using [C2001: Bachelor of Computer Science](https://handbook.monash.edu/2022/courses/C2001?year=2022):
* The course is broken down into Part A, Part B, Part C, Part E and Part F.
* Each part is composed of either **core units**, **elective units** or a **specialisation/major/minor**
* Since students have to take each part in sequence, the parts are wrapped inside a model object called `Wrapper`.
* A `Wrapper` contains >= 1 `CourseModule`, each `CourseModule` has a list of `Core` and `Elective`.
* In cases where students are able to choose multiple `CourseModule` (e.g. different majors or minors), a threshold is set for a `Wrapper` that holds multiple `CourseModule`. 

![graph](https://i.ibb.co/z56T0zV/diagram.png)
In order for a student enrolled in **C2001** to graduate:
* The student must first complete **C2001AB** (`threshold=1` indicates they must complete the sole `CourseModule` inside the `Wrapper`)
	* **C2001AB** include core units FIT1008, FIT1045, FIT1047, FIT2004, FIT2014, MAT1830, MAT1841 and no elective units.
* To complete this `CourseModule`, the student must complete all of the core units listed. After this is completed, the algorithm moves on to the next `Wrapper` (containing **COMPSCI03** and **DATASCI01**)
* The two `CourseModule` inside this `Wrapper` are labelled as Specialisation, but functions the same as any other wrapper, each having a core list and an elective list required.
* Since the `threshold` is only 1, a student only has to take either **COMPSCI03** or **DATASCI01**, not both, in order to move on.
* The algorithm continously processes each wrapper as described above. Once it reaches the end, it checks whether the student has enough remaining units that reach the required free elective credit points to graduate.

The algorithm is designed in a way where it's flexible enough to accommodate any course structure provided in the handbook. For example, [A2006: Bachelor of Arts](https://handbook.monash.edu/2020/courses/A2006) would have a graph that looks like this:
![](https://cdn.discordapp.com/attachments/912362084359090230/924547805253632000/unknown.png)
### How are course requirements updated and maintained?
If the proposed solution is used in the future, a new user-friendly page will be created for related staffs to create and update requirements based on the handbook. Once a course is added, any CSV files of students enrolled in the course can be processed easily.


### What about courses that have not been updated?
In order to handle new courses that have yet to be added to the application system database, BoEasy will display a different invalid symbol (🟥) to indicate that the course is not recognised.

When CSV files contain students enrolled in courses that are not in the database, they will be marked as shown below.
![FinalPage2](https://i.ibb.co/QkYpktP/image.png)

## Selection Criteria
#### Cost of Implementation
Hosting the applicaton system on an `t4g.small` [AWS EC2](https://aws.amazon.com/ec2/pricing/on-demand/) instance should be sufficient for the scale of this application and would cost ~150 USD per year.

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
