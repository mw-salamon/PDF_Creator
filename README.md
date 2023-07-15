# PDF Creator web application

## Description

My motive behind creation of this app was to design a universal tool, which could be expandable and could automate a bit of my work in the company that i was assosiated with. It's pretty basic application, but it let me learn basics of writting small web apps with Flask. I could also train my JavaScript skills, as well as HTML / CSS. The design is basic. It allows the user to choose one of a few templates to create, a customizable PDF. Right now there is only one, which allows to create basic PDF for setting currency exchange prices and automatically downloading it to users computer.

In the future I hope to expand the template list and have my life even more convenient. Also I could add features like saving few of the pdfs that were created if the user would like to download them again. Also to make it even more personal I could implement sign in, for each user to have their own pdfs.

The app is also deployed on AWS EC2 instance and database is deployed on AWS RD. You can check it by entering the url: `http://pdfcreatorkfps.com/`

### Tech Stack:
- Python
- Flask
- FPDF
- SQL Alchemy
- MySQL
- HTML/CSS
- JavaScript
- Nginx
- Gunicorn

## Installation

Here is a basic guide to run the app on your own computer, to check it out:

- Before installing the app you should have already downloaded git and python on your computer
- Open terminal on your computer and type in: 
  `git clone https://github.com/Ezqull/fit-connect`
- Then type: 
  `cd fit-connect`
- To install all needed dependencies you need to create your own virtual environment. To create it I recommend watching one of these tutorials:
1. For Windows: https://www.youtube.com/watch?v=APOPm01BVrk
2. For Mac/Linux: https://www.youtube.com/watch?v=Kg1Yvry_Ydk
- To download needed libraries you need to activate your venv (it is shown in the tutorials) and type command:
  `pip install -r requirements.txt`
- Open the foler in your favourite IDE (I recommend **VS Code**)
- In line 14th of the *__init__.py* file, change the database url to your own. For MySQL database, the URI should look like this: `mysql+mysqldb://username:password@localhost:port/db_name`
- Then all the things should be set and you should be able to start the application. You can do it in two ways, with console or in your IDE.
1. To launch app from console type in default project catalog:
`python app.py`
<<<<<<< HEAD
2. To launch app from console just click RUN button in the top right corner of the screen (For VS Code)
=======
2. To launch app from console just click RUN button in the top right corner of the screen (For VS Code)
>>>>>>> 4073acb9917816f4c40302c5445bf0c446d2441e
