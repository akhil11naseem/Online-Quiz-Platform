# TYPEit Quiz Platform


Varun Jain 21963986
Akhil Naseem 22237476
Lance Chew


Welcome to the TYPEit Web App! This project is packaged as a Flask Application using SQLite as a database engine. 
This is an interactive quiz aimed at high school students aged between 13-17 with a variety of different subjects and 
a range of difficulty to offer a broad spectrum of challenge to all users.

This app allows for the login of both administrator and student type accounts and also the registration for new students as 
the class grows. Admins may control who can log into the quiz and also what subjects are available for the students to attempt.
The students may then choose which of the available subjects they would like to try, which each have a corresponding question 
set.

During the quiz, users will be presented with a question and a clue as to what letter the answer starts with just to get them 
going. It is then up to the user to input the correct word which will award points based on how many you get correct. As the 
user inputs the word, the line will turn green if the user is on the right path, and turn red if they begin to input wrong 
characters. Beware, there is a timer that is ever diminishing, if you fail to answer all questions before the timer runs out, 
your quiz run will end! If you get stuck on a word, do not worry, the skip button will allow continuation to the next word.

At the student dashboard, there will be a results table that will display the best score attained for each subject. 
Admins will also be able to see the highest score attained for each subject by the students.


## User Story

1.	The user will be directed to a login page and asked for a username and password. This combination will be validated through the database and the login button will bring the user to the appropriate dashboard.
2.	If the user has no existing account, one may be created using the registration page which allows for a custom username and password to be entered. By default, all created user accounts will be given student access only and additional admin access will have to be added manually from the backend.
3.	The student dashboard opens up into the topic selection page, with sidebar options allowing the student to view his high scores in each subject as well as the highest score attained by classmates.
4.	The student may then choose a topic from the selection available on the choose topics page which will then bring them to the question page.
5.	The question page consists of a score/streak counter on the top left, a timer on the top middle of the screen and the question in the centre with an input field pre-filled with a hint to start the student off.
6.	As the user types in their attempt, the input field will gradually fill green proportional to how complete the word is. If the letter entered is incorrect, the bar will switch to red, notifying the student that the letter entered is wrong.
7.	The user only needs to successfully type the full correct answer to submit the answer and the next question will automatically load with the previous answer appended with a tick on the left hand side.
8.	If the user chooses to skip the word, score will not be awarded and the answer will be appended with a cross on the left-hand list.
9.	Upon completion, the student will be brought to a results screen showing the quiz outcome and a button to return to the dashboard to pick another topic.


## Admin Story

1.	Admins may login with the default admin login.
2.	The admin dashboard will open up automatically starting at the choose topics screen where admins may choose to enable or disable topics.
3.	Along the left bar, the manage students tab will bring up a page where admins are able to enable/disable login for students using a checkbox function.
4.	Admins may also view the class scores for each topic and the highest score attained overall.



## Modules 

* [Flask](https://pypi.org/project/Flask/) - `pip install Flask`
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) - `pip install flask-sqlalchemy`
* [Flask-Login](https://flask-login.readthedocs.io/en/latest/) - `pip install flask-login` 
* [Flask-migrate](https://flask-migrate.readthedocs.io/en/latest/) - `pip install Flask-Migrate` 

## Technologies 
* Client Side 
  * HTML 
  * CSS
  * Bootstrap 
  * Javascript 
  * JQuery - allows for DOM manipulation and Ajax requests
  
* Server Side 
  * Flask 
  * SQLite 
  *	SQLAlchemy
  * Jinja2 Templating for HTML
  
* Git Bash and Github

## Methodology
  1. Throughout this project, we used trello as our base group to keep track of what had to be completed, what was completed, and who was assigned each task. We first discussed and planned about the potential quiz platform ideas, and created a basic template of what we thought would be appelling to us and the audience


## Routes 
* Open Routes 
  * `http://localhost/` - Login Page 
  * `http://localhost/login` - Login Page 
  * `http://localhost/register` - Registration page
  
* Protected Routes 
  * Admin Routes 
    * `http://localhost/select-topics` - add/take away topics by enabling/disabling the topics 
    * `http://localhost/manage-students` - disable/enable students, and have the option to delete users who are not welcomed
    * `http://localhost/class-scores`  - shows the scores of each students after they finish a quiz 
  * Student Routes 
    * `http://localhost/choose-topic-test` - provided with a range of options with quiz topics
    * `http://localhost/my-scores`  - shows the students their individual scores, alongside with the highest score in the class

## Instructions 

* Download the respository 
* Navigate throught the respoitory to the `Main Folder`
* Set up the virtual environment through the following commonds on the terminal 
  *`python3 -m venv venv` 
  * `source venv/bin/activate` for macOS or `source venv/Script/activate` for Windows
  * `pip install -r requirements.txt`
  * `flask run`
  * `Open browser to the local host URL:`http://127.0.0.1:5000`

## Testing
### Manual Testing using uniitests 
  
#### Cross Browser Compatible
  * Works on all three engines: Internet Explorer, Firefox and Google Chrome 
#### Code Validation 
  * Works prefectly for the following validators checks for HTML and CSS on [W3C](https://validator.w3.org/)
#### Backend Testing 
  * The Application that i have tested is the quiz platform TYPEit. I have computed comprehensive tests for the login and register system. Some include:
    1. ensuring that the user logins with the correct credentials, 
    2. ensure that no unregistered user can access the system without proper authentication, 
    3. no duplicate useranmes, new user cannot register with a username that is already in the database
    4. Ensure pages get redirected to the right loctions, no mismatch between the admin and student links 
    5. Ensures admin can only access the admin links, and students can only access links provided to them in the game. 
    
#### How to Execute 
  * ensure you are within the `Main Folder` directory,
  * on the terminal run: `python3 -m flask_app.tests.backend`
  
### Automation Testing using selenium testing
  * For the TYPEit quiz application, i have computed fully automated tests using unittests. This is executable on firefox. I have ran 5 seperates tests
    1. New User trys to make an new account on `http://localhost/register`, however authentication fails as there is already a pre-existing username in the database. In return the following messages appears on the screen: `This username is taken, try again.`
    2. New User makes an new account with a unquie username. The register page redirects to the login, and user can access the contents
    3. The admin logins with its username and password, and can access all the following pages: `/select-topics`, `/Class-scores`,`/Manage-students`
    4. The student logins in with its username and password, and can access all the following wpages `/choose-test-topic`, `/my-scores`
    5. Finally, a automated test where the students logins in with its details, and plays a quiz. I give a automated demonstration of a student playing the quiz, and recieving its scores. 

#### How to Execute 
  * ensure you are within the `Main Folder` directory, 
  * on the terminal run: `python3 -m flask_app.tests.frontend`
  
## Potential Future Features 
* Give the users and admin the flexability to change their password and username
* Flexability towards the question set variation, for instance: pictionary
* have a really big databse, to give mix the order of the question set 

## Project Structure 

The following image is the database structure we implemented in our TYPEit Quiz Platform 
* The database consists of three categories: User, Results and Topic. 
  * User table holds the specific id of all users, login information, their hashed password, privilege details of each user and a Boolean value that denotes whether or not the student account is enabled by the admin.
  * The result table is the link between the User Table and the topic table, it stores a users id and the result of a specifc topic 
  * The The topic table holds the unique id of the different topics for the quiz, its name and its associated question sets to be selected by the student.
  
  
  ## Directory Layout 
  
    .
    ├── TYPEit
    ├── Main Folder                   
    │   ├── migrations     
    │   ├── requirements.txt    
    │   ├── flask_app          
    │       ├── routes 
    │       │   ├── __init__.py
    │       │   ├── auth.py
    │       │   ├── main.py
    │       │
    │       ├── templates 
    │           ├── Admin Dashbord 
    │
    │
    │
    │
    ├──         
    └── ...
  
  
  
  
## Design 
