## Cloud.gov Setup
This project covers documenting the process of setting up a python + flask project within the Cloud.gov space.

We will be using cloud.gov Identity Provider (IDP) and an Amazon Webservice Relational Database Service (AWS RDS).


### Setup
Our primary application will be called `template-flask` it will be using `template-flask-uaa` which is connected to cloud.gov IDP and `template-flask-db` which is the RDS.

To set up the IDP you will either go through the User Interface (UI) or by running the following commmand:
```
cf create-service cloud-gov-identity-provider oauth-client my-uaa-client
```

Similar command to create the database.
```
cf create-service aws-rds small-mysql my-db
```
> Running this command will detach from the process, creating the database will take a decent amount of time.

Database information including username, password and JDBC (Java Database Connectivity) with be within the environmental variables. Accessed with `os.environ`.


### Obtaining Credentials
To get the nessecary credentials for utilizes cloud.gov UAA you need to create the service key which will be provided to your application. This can be done with the below command:

```
cf create-service-key \
    template-flask-uaa \
    my-service-key \
    -c '{"redirect_uri": ["https://template-flask.app.cloud.gov/auth/callback", "https://template-flask.app.cloud.gov/auth/logout"]}'
cf service-key my-uaa-client my-service-key
```

> The redirect_uri will be the redirect uris which the user will be sent to **after** the authenticated login, whatever url you wish to intercept the information will be that url. It will also include the `/logout` url which properly disconnects the user.

### Credentials
Reading the documentation provided by cloud.gov you need to ensure your application has credentials which match the request. To do so I had to manually set environmental variables which then are accessed within the application. This ensures the information is not passed. You can do this through the GUI or the below command:

```
>>> cf service-key template-flask my-service-key
{
  "credentials": {
    "client_id": "12345678-1234-1234-1234-12345672890",
    "client_secret": "1234567890qwertyuiopasdfghjkl"
  }
}
>>> cf set-env template-flask client_id 12345678-1234-1234-1234-12345672890
>>> cf set-env template-flask client_secret 1234567890qwertyuiopasdfghjkl
```


## Testing Environment Setup
If you are trying to run locally vs in production you need to ensure that all of the connected routes and redirect_uris are properly set for the seperate environments.

### Local UAA
```
docker run -d --name uaa-uaa -p 8080:8080 \
  -e UAA_CONFIG_URL=https://raw.githubusercontent.com/18F/cg-demos/master/cg-identity/uaa.yml \
  hortonworks/cloudbreak-uaa:3.6.3
```