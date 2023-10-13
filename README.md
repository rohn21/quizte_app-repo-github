
# Quizte - quizapp using Python-Django(CBV)

Quizte is a web application built using Python and Django. It's designed to facilitate online quizzes where teachers can create quizzes and students can attend them. Here's a more detailed description:

**Role-Based Registration and Authentication:** The application supports `different user roles (multiple user types)`, specifically teachers(as an admin) and students. The registration and authentication system is designed to handle these different roles, ensuring that each user has access to the appropriate features.  This is implemented using Django’s `AbstractUser model`, which provides a flexible and extensible user model.

**Quiz Creation:** Teachers can create quizzes using Django's `inline_formset_factory`. This allows them to easily add multiple related objects (like questions for a quiz) at once, providing a seamless user experience.

**Quiz Attendance:** Students can attend the quizzes created by teachers. They can navigate through the questions, submit their answers, and receive a score at the end.

**Class-Based Views:** The application makes extensive use of `Django's class-based views`. These provide a more structured way to define views and offer more flexibility and reusability compared to function-based views.

**Permission Checks:** The application uses Django's `LoginRequiredMixin` as well as `decorators` for `permission` checks. This ensures that only authenticated users can access certain views, and that users can only access data that they're authorized to see.

**Results Display:** After a student completes a quiz, they can view their results. This includes their score and other relevant details.

It provides a practical solution for online learning environments, enabling teachers to easily create quizzes and students to attend them from anywhere.

## Installation
If you haven't, you need a working knowledge of Django and a working Django Project before you can use this Django webapp. A good place to start is [here](https://docs.djangoproject.com/en/4.2/intro/tutorial01/#creating-a-project). Make sure you refer to the django version you are using. A quick way to start a new django project is to run the following command:

- Install Django:
```bash
 pip install django
```
- Install Python Pipenv:
```bash
 pip install pipenv
```

- Go to your desired development folder and create a new django project:
```bash
 django-admin startproject quizapp && cd quizapp
```
Install Django on you virtual environment:
```bash
 pipenv install django
```
Add app_name to INSTALLED_APPS in you new Django Project:
```bash
 INSTALLED_APPS = [
    ...,
    'usrs',
    'quiz',
    'crispy_forms',
    'crispy_bootstrap4',
    'bootstrap4',
    'widget_tweaks',
    ...,
]
```
Perform database migrations:
```bash
 python manage.py migrate
```
Add Django SuperUser and follow the prompts.:
```bash
 python manage.py createsuperuser
```
## How To Set Up Quizte for Development

1. Navigate to your projects directory.
2. Clone the repo from github and CD into project.


```bash
  git clone https://github.com/rohn21/quizte_app-repo-github.git
```

- Go to the project directory

```bash
  cd quizapp
```

- Activate the local environment

```bash
virtualenv env
source env/bin/activate
```

- Install the requirements

```bash
  pip3 install -r requirements.txt
```

- Migrate the database

```bash
./manage.py makemigrations
./manage.py migrate
```

- You can run the server by using command

```bash
./manage.py runserver
```


## Features

- Light/dark mode toggle



## Lessons Learned

This project demonstrates a good understanding of CRUD operation as well as Django's advanced features, including ORM Concepts, class-based views, formsets, queryset , sessions and authentication.


## Possible future updates

Here are some potential future updates in Quizte:

1. **Question Types:** Currently, it seems like your application supports only one type of question. You could add support for multiple choice questions, true or false questions, fill in the blank questions, and more.

2. **Quiz Difficulty Levels:** Allow teachers to set a difficulty level for each quiz (e.g., beginner, intermediate, advanced). This would help students choose quizzes that are appropriate for their skill level.

3. **Time-Limited Quizzes:** Add the option for quizzes to be time-limited. Once a student starts a time-limited quiz, they would have a certain amount of time to complete it.

4. **Leaderboards:** Implement a leaderboard system that ranks students based on their quiz scores. This could encourage healthy competition and motivate students to improve.

5. **Analytics:** Provide teachers with analytics about quiz performance. For example, you could show how many students have taken each quiz, the average score, etc.

6. **Feedback Mechanism:** Allow students to provide feedback on quizzes. This could help teachers improve their quizzes and teaching methods.

7. **Notifications:** Implement a notification system to alert students when new quizzes are available or when they receive feedback on a completed quiz.

## 🛠 Skills
Python, Django, Javascript, HTML, CSS


## Badges


[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)


## Feedback

If you have any feedback, please reach out to me at rohn21@outlook.com

