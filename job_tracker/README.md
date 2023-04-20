OSU CS467 Capstone Group Project - Job Tracker

Motivation:
Students often apply to dozens of positions within an application cycle. There also are many factors that exist to increase the difficulty for students to manage their applications. For example, the hiring process for each company is different. It may take several weeks to several months and include many different statuses(i.e. applied, waiting to hear back, interviewed, rejected, etc.). This web application is designed to help CS students to track their job-hunting efforts in a more intuitive way.

Structure:
The structure of the Job Tracker project is 3-tier architecture which are client tier, application tier, and database tier. The client tier(frontend) was written by ReactJs. The application tier(backend) was written by NodeJs Express framework in RESTful API format. And a MongoDB database was utilized for the database tier. The client tier sends HTTP requests to the application tier. Then, the application tier interacts with the database tier to get/add/update/delete data accordingly. Finally, the application tier responds to the client tier with data for displaying.
