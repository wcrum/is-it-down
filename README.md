# Is It Down?

**Prologue:** `Is it down?` is a server side rendered application intended to show the statuses of domains. Influence from isitdown.com and downdetector.com but with a twist of being OS and developed with an intended use of tactical domains. This application intends to be as lightweight as possible, meaning with a few configuration files a docker container you can replicate this yourself. The backend is written in Python which utilizes Flask as a lightweight webserver framework which is connected to a MySQL instance. I am not a frontend developer, I am utilizing Bootstrap 5 and jQuerey to interact with the backend when needed. I am trying to limit the communication the frontend has with the back to maintain security, hence server side rendered. I intend to move the Bootstrap to use USWDS components.

## Development
### Backend
![Python](https://img.shields.io/badge/Python-3670A0?&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/Flask-%23000.svg?&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-00778f.svg?&logo=mysql&logoColor=white)

Using Python 3.x

### Frontend
![jQuery](https://img.shields.io/badge/jQuery-%230769AD.svg?&logo=jquery&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap%205-%23563D7C.svg?&logo=bootstrap&logoColor=white)


### Security
![Jasmine](https://img.shields.io/badge/Snyk-%23563D7C.svg?&logo=snyk&logoColor=white)
[![Known Vulnerabilities](https://snyk.io/test/github/elisoncrum/is-it-down/badge.svg)](https://snyk.io/test/github/elisoncrum/is-it-down/badge.svg)
## Templating
This application was built using my own Full-Stack template which is intended for cloud.gov Cloud Foundrys platform.

[elisoncrum/cloud-gov-flask-template](https://github.com/elisoncrum/cloud-gov-flask-template)

# Important Links
- https://cloud.gov/docs - Primary Documentation for cloud.gov
- https://github.com/cloud-gov/cg-demos - Demos for cloud.gov applications
