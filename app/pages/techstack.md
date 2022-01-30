---
Title: Techstack
Summary: Template cloud.gov Application
Authors: William Crum
Date: January 23, 2022
show_toc: True
---

## How was it built?

### Pages
The pages are `.md` files which are converted and compiled at application initializaion. They have meta information which is then referenced by Flasks router. If the route doesnt match an existing route it will abort. Using this method a developer can utilize fast page development (like Jekyll) using `.md` files and more advanced pages that are server side rendered. Using a mix of Jekyll and Jinja a developer can use some "advanced" markdown rendering and include server side objects like this.... 

```This page was rendered at {{ time }}!```

### Authentication
Authentication leverages cloud.gov User Account and Authentication (UAA). At login an application redirects the user to the UAA, the application provides information based on the context of the app, the UAA returns information which we then post stating the user has logged in. 

## Backend Development
The backend is written in Python and Flask with SQLModel as the ORM, using AWS RDS MySQL as the database. 

### Backend Connectors
This template utilizes Gunicorn Web Server Gateway Interface for the production application. I used PyMySQL for the driver, for larger production application see [openstack.org driver evaluation](https://wiki.openstack.org/wiki/PyMySQL_evaluation) to see which driver works best for you.

### Technologies and Reasoning
**Flask**: I ended up using Flask because I knew it had capabilities as an API and a server side render, FastAPI is a good alternative if you compile / serve the Front End Seperatly, for the scope of this project it just fit best

**SQLModel** SQLModel is a mix between SQLAlchemy and Pydantic, it saves the hassle of confusing types between the database and the backend


[![](https://github-readme-stats.vercel.app/api/pin/?username=elisoncrum&repo=cloud-gov-flask-template)](https://github.com/elisoncrum/cloud-gov-flask-template)

## Frontend Development
Out of everything I have developed, frontend is by far my worst enemy. Having a client side rendered application if you are looking for an application to be more "reactive." Use it. I decided to use Jinja2 alongside Bootstrap 5 and other libraries to help me get the intended template.

### Code Highlighthing
Code highlighting is one of those things that is appreciated when you dont realize you are looking at it. I personally hated looking at unstyled code. Using Markdown2 and the extension `fenced-code-block` you can achieve just the same.

```python
def add_numbers(x: int, y: int) ->:
    return x + y
```